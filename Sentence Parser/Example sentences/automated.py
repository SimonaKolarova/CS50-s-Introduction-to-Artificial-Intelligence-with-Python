import os

def main():
    for i in range(1,11): 
        # This is to tell you which file it is currently processing before 
        # the output of your code
        print(f"{i}\n", flush = True)
        os.system("python parser.py " + str(i) + ".txt")
    print(f"Additional\n", flush = True)

    #os.system("python parser.py ")
    # His Thursday chuckled in a paint.
    #os.system("Holmes sat in the the armchair.") 


if __name__ == "__main__":
    main()