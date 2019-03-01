import sys

from spotify import api

def main(artist, country_code):
    result = api.top_tracks(artist, country_code)
    print()
    for item in result['tracks']:
        print(item['name'])
    print()



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2].upper())
