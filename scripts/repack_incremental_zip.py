import os
import zipfile
import datetime
import shutil
import subprocess
import argparse
import sys

# Monkeypatch ZipInfo to ALWAYS set the UTF-8 flag (Bit 11)
orig_encode = zipfile.ZipInfo._encodeFilenameFlags
def force_utf8_encode(self):
    fname, flags = orig_encode(self)
    return fname, flags | 0x800
zipfile.ZipInfo._encodeFilenameFlags = force_utf8_encode

# Resolve paths relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

SOURCE_DIR = os.path.join(PARENT_DIR, 'codex-skills')
BACKUP_DIR = os.path.join(PARENT_DIR, 'backups')
INCREMENTAL_DIR = os.path.join(PARENT_DIR, 'incremental_packs')

EXCLUDE_DIRS = {'.git', '.github', '__pycache__', 'node_modules', '.DS_Store', '__MACOSX', '.vscode', '.idea', '15_社科研究与实证工具'}
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

def backup_existing_zip(output_zip_path, base_sha, target_sha):
    if os.path.exists(output_zip_path):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        mtime = os.path.getmtime(output_zip_path)
        dt = datetime.datetime.fromtimestamp(mtime)
        timestamp = dt.strftime('%Y%m%d-%H%M%S')
        backup_name = os.path.join(BACKUP_DIR, f'codex-skills-incremental-from-{base_sha}-to-{target_sha}.backup-{timestamp}.zip')
        
        # If backup file already exists, append current time
        if os.path.exists(backup_name):
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y%m%d-%H%M%S')
            backup_name = os.path.join(BACKUP_DIR, f'codex-skills-incremental-from-{base_sha}-to-{target_sha}.backup-{timestamp}.zip')
            
        print(f"Backing up existing {output_zip_path} to {backup_name}...")
        shutil.copy2(output_zip_path, backup_name)
        print("Backup created successfully.")

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True, cwd=PARENT_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(args)}\nError: {res.stderr}")
    return res.stdout

def get_changes(base_ref):
    # Verify git repository
    if not os.path.exists(os.path.join(PARENT_DIR, '.git')):
        print("Error: PARENT_DIR is not a git repository.")
        sys.exit(1)
        
    # Verify base_ref exists
    try:
        run_cmd(['git', 'rev-parse', base_ref])
    except Exception:
        print(f"Error: Git reference '{base_ref}' is invalid.")
        sys.exit(1)
        
    print(f"Calculating changes against base reference: {base_ref}")
    
    modified_added = set()
    deleted = set()
    
    # 1. Get status since base_ref (both staged, unstaged, and committed)
    diff_output = run_cmd(['git', '-c', 'core.quotePath=false', 'diff', '--name-status', base_ref])
    for line in diff_output.splitlines():
        if not line.strip():
            continue
        parts = line.split('\t')
        status = parts[0]
        if status.startswith('R'): # Renamed
            old_path = parts[1]
            new_path = parts[2]
            deleted.add(old_path)
            modified_added.add(new_path)
        elif status == 'D': # Deleted
            path = parts[1]
            deleted.add(path)
        else: # Added, Modified, Type changed, etc.
            path = parts[1]
            modified_added.add(path)
            
    # 2. Get untracked files
    untracked_output = run_cmd(['git', '-c', 'core.quotePath=false', 'ls-files', '--others', '--exclude-standard'])
    for line in untracked_output.splitlines():
        if line.strip():
            modified_added.add(line.strip())
            
    # Helper to check if a path is in codex-skills and not excluded
    def is_valid_change(path):
        # Must be in codex-skills/
        if not (path.startswith('codex-skills/') or path.startswith('codex-skills\\')):
            return False
        # Must not be excluded
        full_path = os.path.join(PARENT_DIR, path)
        if should_exclude(full_path):
            return False
        return True
        
    valid_modified_added = sorted([p for p in modified_added if is_valid_change(p)])
    valid_deleted = sorted([p for p in deleted if is_valid_change(p)])
    
    # Make sure we don't list a file as deleted if it's currently tracked/present
    final_deleted = []
    for p in valid_deleted:
        if p not in valid_modified_added:
            final_deleted.append(p)
            
    return valid_modified_added, final_deleted

def find_skill_root(rel_path):
    # rel_path is like 'codex-skills/46_小红书热门营销文案与自动化控制小红书账号/MediaCrawler/api/main.py'
    parts = rel_path.split('/')
    if len(parts) == 1:
        parts = rel_path.split('\\')
    # Check directories from leaf upwards (skip the filename itself)
    for i in range(len(parts) - 1, 0, -1):
        check_dir = os.path.join(PARENT_DIR, *parts[:i])
        if os.path.exists(os.path.join(check_dir, 'SKILL.md')):
            return '/'.join(parts[:i])
    return None

def parse_skill_metadata(skill_rel_path):
    skill_md_path = os.path.join(PARENT_DIR, skill_rel_path, 'SKILL.md')
    if not os.path.exists(skill_md_path):
        return None
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---')
            if len(parts) >= 3:
                yaml_block = parts[1]
                metadata = {}
                current_key = None
                current_val_lines = []
                
                for line in yaml_block.splitlines():
                    stripped = line.strip()
                    if not stripped:
                        continue
                    # Check if line starts a new key
                    if ':' in line and not line.startswith(' '):
                        if current_key:
                            metadata[current_key] = " ".join(current_val_lines).strip().strip('"').strip("'")
                        
                        k, v = line.split(':', 1)
                        current_key = k.strip().lower()
                        v_stripped = v.strip()
                        if v_stripped in ('>', '|'):
                            current_val_lines = []
                        else:
                            current_val_lines = [v_stripped]
                    else:
                        if current_key:
                            current_val_lines.append(stripped)
                            
                if current_key:
                    metadata[current_key] = " ".join(current_val_lines).strip().strip('"').strip("'")
                return metadata
    except Exception as e:
        print(f"Warning: Failed to parse metadata for {skill_rel_path}: {e}")
    return None

def build_incremental_zip(base_ref):
    # Resolve short SHAs for base and target
    base_sha = run_cmd(['git', 'rev-parse', '--short', base_ref]).strip()
    target_sha = run_cmd(['git', 'rev-parse', '--short', 'HEAD']).strip()
    
    modified_added, deleted = get_changes(base_ref)
    
    if not modified_added and not deleted:
        print("No changed files under 'codex-skills/' since base reference.")
        print("Incremental package is empty. Aborting.")
        return
        
    print(f"\n--- Change Summary ---")
    print(f"Base commit: {base_sha}")
    print(f"Target commit: {target_sha}")
    print(f"Added / Modified files: {len(modified_added)}")
    print(f"Deleted files: {len(deleted)}")
    print(f"----------------------\n")
    
    incremental_name = f'codex-skills-incremental-from-{base_sha}-to-{target_sha}.zip'
    os.makedirs(INCREMENTAL_DIR, exist_ok=True)
    output_zip_path = os.path.join(INCREMENTAL_DIR, incremental_name)
    temp_zip_path = os.path.join(INCREMENTAL_DIR, f'codex-skills-incremental-from-{base_sha}-to-{target_sha}_new.zip')
    
    backup_existing_zip(output_zip_path, base_sha, target_sha)
    
    print(f"Building incremental ZIP at {temp_zip_path}...")
    
    count = 0
    added_dirs = set()
    base_arc_dir = 'codex-skills'
    
    # Generate release log text
    log_lines = [
        "Incremental Release Package",
        "===========================",
        f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Base Commit: {base_sha}",
        f"Target Commit: {target_sha}",
        "",
        "Commit Logs:",
        "-----------"
    ]
    try:
        git_logs = run_cmd(['git', 'log', '--oneline', f'{base_sha}..{target_sha}'])
        if git_logs.strip():
            log_lines.append(git_logs.strip())
        else:
            log_lines.append("No committed logs (working tree contains uncommitted/untracked changes).")
    except Exception as e:
        log_lines.append(f"Failed to fetch logs: {e}")
    log_content = "\n".join(log_lines) + "\n"
    
    # Identify affected skills
    affected_skills = {}
    for rel_path in modified_added:
        skill_root = find_skill_root(rel_path)
        if skill_root and skill_root not in affected_skills:
            meta = parse_skill_metadata(skill_root)
            affected_skills[skill_root] = meta or {"name": os.path.basename(skill_root), "description": "No description available."}
            
    # Generate README.md Agent Guide
    readme_lines = [
        f"# Codex Skills Incremental Update ({base_sha} ➔ {target_sha})",
        "",
        "Welcome, AI Agent!",
        "",
        "This package contains an incremental update for the **Codex Skills Library**.",
        "",
        "## 📥 Integration Guide",
        "Please integrate these updated contents into your active workspace and skill library context:",
        "- **Apply Changes**: Merge the files in `codex-skills/` into your current workspace's skill library directory, overwriting existing files.",
        "- **Handle Deletions**: If files have been removed, consult `deleted_files.txt` at the root of this package to clean up removed paths in the workspace.",
        "- **Register Skills**: Register the newly added skill directories (detailed below) into your customizations configuration or customization roots (such as `.agents/skills.json` or your runtime's equivalent settings) so they are discoverable and active.",
        "",
        "---",
        "",
        "## 🚀 Updated Skills in this Package",
        "The following skills have been added or updated in this release:"
    ]
    
    for idx, (skill_root, meta) in enumerate(sorted(affected_skills.items(), key=lambda x: x[1].get('name', ''))):
        name = meta.get('name', os.path.basename(skill_root))
        desc = meta.get('description', 'No description available.')
        readme_lines.extend([
            f"### {idx+1}. **{name}**",
            f"* **Path**: `{skill_root}`",
            f"* **Description**: {desc}",
            ""
        ])
        
    readme_lines.extend([
        "---",
        f"*Generated automatically on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Refer to `release_log.txt` for detailed commit history.*"
    ])
    readme_content = "\n".join(readme_lines) + "\n"
    
    with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Add root dir
        zinfo_root = zipfile.ZipInfo(base_arc_dir + '/')
        zinfo_root.external_attr = 0x41ED0000
        zf.writestr(zinfo_root, b'')
        added_dirs.add(base_arc_dir)
        count += 1
        
        # Add README.md to ZIP
        zinfo_readme = zipfile.ZipInfo('README.md')
        zinfo_readme.external_attr = 0x81A40000 # normal file
        zinfo_readme.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(zinfo_readme, readme_content.encode('utf-8'))
        print("Added README.md to archive.")
        count += 1
        
        # Add release_log.txt to ZIP
        zinfo_log = zipfile.ZipInfo('release_log.txt')
        zinfo_log.external_attr = 0x81A40000 # normal file
        zinfo_log.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(zinfo_log, log_content.encode('utf-8'))
        print("Added release_log.txt to archive.")
        count += 1
        
        # If there are deleted files, write deleted_files.txt inside the ZIP
        if deleted:
            # Paths inside deleted_files.txt should match their zip archive path (e.g. codex-skills/...)
            deleted_content = "\n".join(deleted) + "\n"
            zinfo_del = zipfile.ZipInfo('deleted_files.txt')
            zinfo_del.external_attr = 0x81A40000 # normal file
            zinfo_del.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zinfo_del, deleted_content.encode('utf-8'))
            print("Added deleted_files.txt to archive.")
            count += 1
            
        # Pack modified and added files
        for rel_path in modified_added:
            file_path = os.path.join(PARENT_DIR, rel_path)
            if not os.path.exists(file_path):
                # Just in case git thinks it exists but it was removed
                continue
            if os.path.islink(file_path):
                continue
                
            # Ensure directories are explicitly added
            # rel_path is like 'codex-skills/category/skill/file.txt'
            parts = rel_path.split('/')
            if len(parts) == 1:
                parts = rel_path.split('\\')
                
            for i in range(1, len(parts)):
                dir_path = '/'.join(parts[:i])
                if dir_path not in added_dirs:
                    zinfo_dir = zipfile.ZipInfo(dir_path + '/')
                    actual_dir = os.path.join(PARENT_DIR, *parts[:i])
                    try:
                        st = os.stat(actual_dir)
                        zinfo_dir.external_attr = (st.st_mode & 0xFFFF) << 16
                    except Exception:
                        zinfo_dir.external_attr = 0x41ED0000
                    zf.writestr(zinfo_dir, b'')
                    added_dirs.add(dir_path)
                    count += 1
            
            # Add file to ZIP
            arcname = rel_path.replace('\\', '/')
            zinfo = zipfile.ZipInfo.from_file(file_path, arcname=arcname)
            st = os.stat(file_path)
            zinfo.external_attr = (st.st_mode & 0xFFFF) << 16
            zinfo.compress_type = zipfile.ZIP_DEFLATED
            
            with open(file_path, 'rb') as f:
                zf.writestr(zinfo, f.read())
            
            count += 1
            if count % 100 == 0:
                print(f"Added {count} entries...")
                
    print(f"Finished building {temp_zip_path}. Total entries: {count}")
    if os.path.exists(output_zip_path):
        os.remove(output_zip_path)
    os.rename(temp_zip_path, output_zip_path)
    print(f"Successfully replaced {output_zip_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build incremental zip of changed files in codex-skills since a git baseline.")
    parser.add_argument('-b', '--base', type=str, default='HEAD~1',
                        help="Baseline git reference to compare against (default: HEAD~1)")
    args = parser.parse_args()
    build_incremental_zip(args.base)
