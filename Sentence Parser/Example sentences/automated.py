import os

def main():
    for i in range(1,11): 
        print(f"{i}\n", flush = True)
        os.system("python parser.py " + str(i) + ".txt")

if __name__ == "__main__":
    main()