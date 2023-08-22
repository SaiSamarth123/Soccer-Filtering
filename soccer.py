import requests


class League:
    def __init__(self, name):
        self.name = name


class Team:
    def __init__(self, name):
        self.name = name


class Player:
    def __init__(self, name):
        self.name = name


class Match:
    def __init__(self, team1, team2, league, date, time, venue):
        self.team1 = team1
        self.team2 = team2
        self.league = league
        self.date = date
        self.time = time
        self.venue = venue


class SoccerAPI:
    BASE_URL = "https://api.example.com/soccer"

    @classmethod
    def get_matches(cls):
        response = requests.get(f"{cls.BASE_URL}/matches", headers={"API-Key": ""})
        if response.ok:
            # Parse the response into Match objects
            matches = []
            for match_data in response.json():
                match = Match(
                    team1=Team(match_data["team1"]),
                    team2=Team(match_data["team2"]),
                    league=League(match_data["league"]),
                    date=match_data["date"],
                    time=match_data["time"],
                    venue=match_data["venue"],
                )
                matches.append(match)
            return matches
        else:
            print("Error fetching matches!")
            return []


def main():
    print("Welcome to Soccer Match Filter!")
    while True:
        print("\nMain Menu:")
        print("1. View Matches")
        print("2. Filter Matches")
        print("3. Exit")
        choice = input("Please choose an option (1-3): ")
        if choice == "1":
            matches = SoccerAPI.get_matches()
            for match in matches:
                print(
                    f"{match.team1.name} vs {match.team2.name} - {match.date} {match.time} - {match.venue}"
                )
        elif choice == "2":
            print("Filtering is not implemented yet!")
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
