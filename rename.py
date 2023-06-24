import os

path = r"Z:\Code\Zelden Ring\graphics\test"
prefix = "tile"
suffix = ".png"
#this python file was used in the renaming of many different graphics
def main():
    os.chdir(path)
    # if os.path.isfile("tile100.png"):
    #     print("that file exists dummy")
    # else:
    #     print("nah u good homie")
    for i in range(0, 256):
        if i < 10:
            zeroes = "00"
        elif i < 100:
            zeroes = "0"
        else:
            zeroes = ""
        #old_name = prefix + zeroes + str(i) + suffix
        old_name = str(i) + suffix
        new_name = str(i + 256) + suffix
        #if os.path.isfile(new_name):
        #    print("not renaming this shit bro i = ", i)
        #else:
        os.rename(old_name, new_name)
        


if __name__ == '__main__':
    main()