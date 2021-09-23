import git


def get_spec_commit(commit_hash: str):
    git_repo = get_project_repository(
        "/home/keyur/Desktop/LinuxWorkingGit/linux")
    return git_repo.commit(commit_hash)


def get_project_repository(path: str):
    repository = git.Repo(path)
    assert not repository.bare
    return repository


def get_diff_between_commits(parent_commit, head_commit):
    return parent_commit.diff(head_commit, create_patch=False)

with open("FinalRQ4.csv", "r") as f:
    cc = f.readlines()

consistent = set()
inconsistent = set()

for i in range(1, len(cc) - 1):
    data = cc[i].split(",")
    if data[8] == 'CONSISTENT':
        consistent.add(data[0])
    else:
        inconsistent.add(data[0])

print("hash|||log_cnt|||add|||del|||mod|||other_changes|||other_ext|||ratio|||isConsistent|||message")
with open("newData.csv", "r") as f:
    cc = f.readlines()
for i in range(0, len(cc)):
    sha, log_cnt = cc[i].split("|||||")
    head_commit = get_spec_commit(sha)
    msg = head_commit.message.split('\n', 1)[0]
    added_count = 0
    deleted_count = 0
    modified = 0
    added = 0
    deleted = 0

    if sha not in consistent and sha not in inconsistent:
        label = "NEW"
    elif sha not in consistent:
        label = "INCONSISTENT"
    else:
        label = "CONSISTENT"

    

    for objpath, stats in head_commit.stats.files.items():
        added_count += stats['insertions']
        deleted_count += stats['deletions']

        if added_count == deleted_count:
            modified = added_count
        elif added_count < deleted_count:
            modified = added_count
            deleted = deleted_count - added_count
        else:
            modified = deleted_count
            added = added_count - deleted_count

    if head_commit.parents:
        for parent_commit in head_commit.parents:
            diff = get_diff_between_commits(parent_commit, head_commit)
            # Added File or Deleted File
            other_changes = False
            # Other than .c File
            other_extentions_chnaged = False
            for file_diff in diff:
                if file_diff.change_type == 'A':
                    other_changes = True
                elif file_diff.change_type == 'D':
                    other_changes = True
                elif file_diff.change_type == 'R':
                    other_changes = True
                elif file_diff.change_type == 'M':
                    if not file_diff.a_path.endswith(".c"):
                        other_extentions_chnaged = True
    ratio = int(log_cnt)/(added+deleted+modified)
    print(str(sha) + "|||" + str(log_cnt.rstrip()) + "|||" + str(added) + "|||" + str(deleted) + "|||" + str(modified) + "|||" + str(other_changes) + "|||" + str(other_extentions_chnaged) + "|||" + str(ratio) + "|||" + str(label) + "|||" + str(msg))
