import sys

sys.path.append(r"testen")

from classes import wall_following

def main():
    w = wall_following.wallFollower()
    w.FollowWall()

if __name__ == '__main__':
    main() 