import os
import subprocess
import sys

def get_git_diff_lines():
    """Calculates the total lines added and deleted in staged files."""
    try:
        # First, check the total size of ALREADY staged files
        print("📦 Checking staged changes...")

        # Get the numstat for staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--numstat"], 
            capture_output=True, text=True, check=True
        )
        
        total_lines = 0
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    added = int(parts[0]) if parts[0] != '-' else 0
                    deleted = int(parts[1]) if parts[1] != '-' else 0
                    total_lines += (added + deleted)
                    
        return total_lines
    except subprocess.CalledProcessError as e:
        print("❌ Error communicating with Git. Is this a git repository?")
        sys.exit(1)

def git_commit_and_push(commit_message):
    total_lines = get_git_diff_lines()
    
    if total_lines == 0:
        print("⚠️ No changes detected to commit.")
        return
        
    print(f"📊 Total lines to commit: {total_lines}")
    
    # 100-line strict limit logic
    if total_lines > 100:
        print(f"\n❌ ERROR: Your changes exceed the 100 lines limit ({total_lines} lines).")
        print("As a professional, keep your commits and pushes atomic, small, and focused.")
        print("Unstaging files to let you split the commits...\n")
        subprocess.run(["git", "reset", "HEAD"])
        sys.exit(1)
        
    print("\n✅ Changes are within the 100-line limit. Proceeding with commit...")
    
    # Commit
    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("\n🚀 Pushing code to origin...")
        
        # Find current branch
        branch_res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
        current_branch = branch_res.stdout.strip()
        
        # Push 
        subprocess.run(["git", "push", "origin", current_branch], check=True)
        print("\n🎉 Process completed successfully! Great job splitting your tasks.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred during commit/push: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_commit.py \"Your milestone update or commit message\"")
        print("Example: python auto_commit.py \"Milestone 1: Project Setup completed\"")
        sys.exit(1)
        
    message = sys.argv[1]
    git_commit_and_push(message)
