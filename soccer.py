import requests


class Match:
    def __init__(self, team1, team2, league, date, time, venue):
        self.team1 = team1
        self.team2 = team2
        self.league = league
        self.date = date
        self.time = time
        self.venue = venue


class APIFootball:
    BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/"
    HEADERS = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": "ab29a72b20b7baa8ee24cf05ff50c146E",
    }

    @classmethod
    def get_matches(cls, league=None, team=None, player=None):
        params = {}
        if league:
            league_codes = cls.get_league_code(league)
            if league in league_codes:
                params["league"] = league_codes[league]
        if team:
            team_codes = cls.get_team_code(team)
            if team in team_codes:
                params["team"] = team_codes[team]

        url = cls.BASE_URL + "fixtures"
        response = requests.get(url, headers=cls.HEADERS, params=params)
        matches = []
        if response.ok:
            for fixture in response.json()["response"]:
                match = Match(
                    team1=fixture["teams"]["home"]["name"],
                    team2=fixture["teams"]["away"]["name"],
                    league=fixture["league"]["name"],
                    date=fixture["fixture"]["date"].split("T")[0],
                    time=fixture["fixture"]["date"].split("T")[1],
                    venue=fixture["venue"]["name"],
                )
                matches.append(match)
        else:
            print(f"Error fetching data! Status Code: {response.status_code}")
            print(response.text)
        return matches

    @classmethod
    def get_league_code(cls, country):
        url = cls.BASE_URL + f"leagues?country={country}"
        response = requests.get(url, headers=cls.HEADERS)
        if response.ok:
            leagues = response.json()["response"]
            league_codes = {league["name"]: league["id"] for league in leagues}
            return league_codes
        else:
            print(f"Error fetching data! Status Code: {response.status_code}")
            print(response.text)
        return {}

    @classmethod
    def get_team_code(cls, team_name):
        url = cls.BASE_URL + f"teams?search={team_name}"
        response = requests.get(url, headers=cls.HEADERS)
        if response.ok:
            teams = response.json()["response"]
            team_codes = {team["team"]["name"]: team["team"]["id"] for team in teams}
            return team_codes
        else:
            print(f"Error fetching data! Status Code: {response.status_code}")
            print(response.text)
        return {}


def display_matches(matches):
    print("\nMatches:")
    for match in matches:
        print(f"Date: {match.date} Time: {match.time}")
        print(f"{match.team1} vs {match.team2}")
        print(f"League: {match.league}")
        print(f"Venue: {match.venue}\n")


def main():
    print("Welcome to Soccer Match Filter!")
    while True:
        print("\nMain Menu:")
        print("1. View Matches by Team")
        print("2. View Matches by League")
        print("3. Exit")
        choice = input("Please choose an option (1-3): ")

        if choice == "1":
            team_name = input("Enter team name: ")
            matches = APIFootball.get_matches(team=team_name)
            display_matches(matches)
        elif choice == "2":
            league_name = input(
                "Enter league name (Country Name e.g. England, Spain): "
            )
            matches = APIFootball.get_matches(league=league_name)
            display_matches(matches)
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
