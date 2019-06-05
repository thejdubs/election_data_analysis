import os
import argparse

def main():
    args = parse_args()

    for filename in os.listdir(args.src_dir): 
        src = os.path.join(args.src_dir, filename)
        dst = os.path.join(args.dest_dir, filename).replace(' ', '_')
          
        # rename() function will 
        # rename all the files
        #print(dst)
        os.rename(src, dst)

def parse_args():
    parser = argparse.ArgumentParser(description="Replace Space < > in file name with Underscore <_>.")
    parser.add_argument('src_dir', help='Source Directory of files.')
    parser.add_argument('-d', '--dest_dir', dest='dest_dir', default=None, help='Destintation Directory for new files (Default=src).')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enables verbose printing.')
    args = parser.parse_args()

    if args.dest_dir is None:
        args.dest_dir = args.src_dir

    return args


if __name__ == "__main__":
    main()