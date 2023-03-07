import argparse
import re
import glob
import os

parser = argparse.ArgumentParser(description="Recursively moves files in subdirectories to the root path. Moves all files if --include or --exclude are not supplied.")
parser.add_argument("path", metavar="PATH", nargs="?", default=".", help="The root path where crawling should begin")

group = parser.add_mutually_exclusive_group()

group.add_argument("--include", type=re.compile, help="Takes a regex pattern, only files matching the pattern will be targeted for retrieval. Matching is done on both files and directories.")
group.add_argument("--exclude", type=re.compile, help="Takes a regex pattern, only files not matching the pattern will be targeted for retrieval. Matching is done on both files and directories.")

def crawl(parent, args):    
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

        if args.exclude and args.exclude.search(child):
            if args.verbose:
                print(f"{child}: file excluded by pattern")
                
            continue
        
        elif args.include:
            if args.include.search(child):
                if args.verbose:
                    print(f"{child}: file included by pattern")
            else:
                continue

        if os.path.isdir(child):
            crawl(child, args)
        else:
            # file moving behavior
            print(f"preparing to move {child}")

if __name__ == "__main__":
    args = parser.parse_args()
    
    print("Crawl in progress... DO NOT CANCEL")
    
    if args.include:
        print(args.include)
        
    elif args.exclude:
        print(args.exclude)
    
    crawl(args.path, args)