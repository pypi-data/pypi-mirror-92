import sys


def main(floors:int,interval:int,network:str):

    current_floor = 1

    while current_floor <= floors:
        first_octeto = network.split(".")[0]
        second_octeto = network.split(".")[1]
        three_octeto = network.split(".")[2]
        four_octeto = network.split(".")[3]


        for room in range(0, interval):
            four_octeto = "{}{}".format(current_floor,room)
            print("{}.{}.{}.{}".format(first_octeto,second_octeto, three_octeto, four_octeto))


        current_floor = current_floor + 1


if __name__ == "__main__":
    try:
       main(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3])
    except :
        print("python3 -m gen_network floors interval network/24")
        pass
