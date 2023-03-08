import argparse
import re
import shutil
import os

parser = argparse.ArgumentParser(description="Recursively moves files in subdirectories to the root path. Moves all files if --include or --exclude are not supplied.")
parser.add_argument("path", metavar="PATH", nargs="?", default=".", help="The root path where crawling should begin")
parser.add_argument("-v", "--verbose", action="store_true", help="Logs extra information")
parser.add_argument("-d", "--dry", action="store_true", help="Only prints move operations. Does not move files.")

group = parser.add_mutually_exclusive_group()

group.add_argument("-i", "--include", type=re.compile, help="Takes a regex pattern, only files matching the pattern will be targeted for retrieval. Matching is done on both files and directories.")
group.add_argument("-x", "--exclude", type=re.compile, help="Takes a regex pattern, only files not matching the pattern will be targeted for retrieval. Matching is done on both files and directories.")

def crawl(parent, args):
    print(parent)
    if not os.path.exists(parent):
        print(f"{parent}: folder does not exist.")
        return
    
    try:
        children = os.listdir(parent)
    except PermissionError:
        print(f"{parent}: permission to read denied.")
        return

    for child in children:
        child = os.path.join(parent, child)

        is_dir = os.path.isdir(child)

        if not is_dir and args.exclude and args.exclude.search(child):
            if args.verbose:
                print(f"{child}: file excluded by pattern")
                
            continue
        
        elif not is_dir and args.include:
            if args.include.search(child):
                if args.verbose:
                    print(f"{child}: file included by pattern")
            else:
                continue

        if os.path.isdir(child):
            crawl(child, args)
        else:
            # file moving behavior
            fname = os.path.split(child)[-1]
            new_path = os.path.join(args.path, fname)
            old_path = child

            if old_path != new_path:
                if args.dry:
                    print("mv", old_path, new_path)
                else:
                    shutil.move(old_path, new_path)

if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.verbose:
        print("Crawl in progress... DO NOT CANCEL")
    
    crawl(args.path, args)

    if args.verbose:
        print("Done")