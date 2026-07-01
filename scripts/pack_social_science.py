import os
import zipfile

# Monkeypatch ZipInfo to ALWAYS set the UTF-8 flag (Bit 11)
orig_encode = zipfile.ZipInfo._encodeFilenameFlags
def force_utf8_encode(self):
    fname, flags = orig_encode(self)
    return fname, flags | 0x800
zipfile.ZipInfo._encodeFilenameFlags = force_utf8_encode

# Resolve paths relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

# Source is specifically the category folder
SOURCE_DIR = os.path.join(PARENT_DIR, 'codex-skills', '15_社科研究与实证工具')
OUTPUT_ZIP = os.path.join(PARENT_DIR, 'codex-skills-15_社科研究与实证工具.zip')
TEMP_ZIP = os.path.join(PARENT_DIR, 'codex-skills-15_社科研究与实证工具_new.zip')

EXCLUDE_DIRS = {'.git', '.github', '__pycache__', 'node_modules', '.DS_Store', '__MACOSX', '.vscode', '.idea'}
EXCLUDE_FILES = {'.DS_Store'}

def should_exclude(path):
    parts = os.path.relpath(path, PARENT_DIR).split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith('._'):
            return True
    filename = os.path.basename(path)
    if filename in EXCLUDE_FILES or filename.startswith('._'):
        return True
    return False

def build_zip():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} does not exist.")
        return

    print(f"Building {TEMP_ZIP} from {SOURCE_DIR}...")
    count = 0
    added_dirs = set()
    
    # We want archive paths to start with 'codex-skills/15_社科研究与实证工具/'
    base_arc_dir = 'codex-skills/15_社科研究与实证工具'
    
    with zipfile.ZipFile(TEMP_ZIP, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Add root dir explicitly
        zinfo_root = zipfile.ZipInfo(base_arc_dir + '/')
        zinfo_root.external_attr = 0x41ED0000
        zf.writestr(zinfo_root, b'')
        added_dirs.add(base_arc_dir)
        count += 1
        
        for root, dirs, files in os.walk(SOURCE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('._')]
            
            # Rel path inside the category
            rel_root = os.path.relpath(root, SOURCE_DIR)
            if rel_root == '.':
                rel_parts = []
            else:
                rel_parts = rel_root.split(os.sep)
                
            # Ensure all parent directories are added to zip
            for i in range(len(rel_parts) + 1):
                sub_parts = base_arc_dir.split('/') + rel_parts[:i]
                dir_arcpath = '/'.join(sub_parts)
                if dir_arcpath not in added_dirs:
                    zinfo_dir = zipfile.ZipInfo(dir_arcpath + '/')
                    actual_dir_path = os.path.join(SOURCE_DIR, *rel_parts[:i]) if rel_parts[:i] else SOURCE_DIR
                    try:
                        st = os.stat(actual_dir_path)
                        zinfo_dir.external_attr = (st.st_mode & 0xFFFF) << 16
                    except Exception:
                        zinfo_dir.external_attr = 0x41ED0000
                    zf.writestr(zinfo_dir, b'')
                    added_dirs.add(dir_arcpath)
                    count += 1
            
            for file in files:
                file_path = os.path.join(root, file)
                if should_exclude(file_path):
                    continue
                if os.path.islink(file_path):
                    print(f"Skipping symlink {file_path}")
                    continue
                
                # Compute arcname starting with codex-skills/15_社科研究与实证工具/
                rel_file = os.path.relpath(file_path, SOURCE_DIR)
                arcname = os.path.join(base_arc_dir, rel_file)
                
                zinfo = zipfile.ZipInfo.from_file(file_path, arcname=arcname)
                st = os.stat(file_path)
                zinfo.external_attr = (st.st_mode & 0xFFFF) << 16
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                
                with open(file_path, 'rb') as f:
                    zf.writestr(zinfo, f.read())
                
                count += 1
                if count % 1000 == 0:
                    print(f"Added {count} entries...")
                    
    print(f"Finished building {TEMP_ZIP}. Total entries: {count}")
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)
    os.rename(TEMP_ZIP, OUTPUT_ZIP)
    print(f"Successfully replaced {OUTPUT_ZIP}")

if __name__ == '__main__':
    build_zip()
