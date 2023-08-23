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
        "x-rapidapi-key": "YOUR_API_KEY_HERE",
    }

    @classmethod
    def get_matches(cls, league=None, team=None, player=None):
        params = {}
        if league:
            params["league"] = league
        if team:
            params["team"] = team
        if player:
            params["player"] = player

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
            print("Error fetching matches!")
        return matches

    @classmethod
    def get_teams(cls, league, season="2023"):
        url = cls.BASE_URL + f"teams?league={league}&season={season}"
        response = requests.get(url, headers=cls.HEADERS)
        teams = {}
        if response.ok:
            for team in response.json()["response"]:
                teams[team["team"]["name"]] = team["team"]["id"]
        else:
            print("Error fetching teams!")
        return teams

    @classmethod
    def get_league_code(cls, league_name):
        response = requests.get(
            "https://v3.football.api-sports.io/leagues", headers=cls.HEADERS
        )
        if response.ok:
            for league in response.json()["response"]:
                if league["league"]["name"].lower() == league_name.lower():
                    return league["league"]["id"]
        print("League not found!")
        return None

    @classmethod
    def get_team_code(cls, team_name, league_code=None):
        url = "https://v3.football.api-sports.io/teams"
        if league_code:
            url += f"?league={league_code}"

        response = requests.get(url, headers=cls.HEADERS)
        if response.ok:
            for team in response.json()["response"]:
                if team["team"]["name"].lower() == team_name.lower():
                    return team["team"]["id"]
        print("Team not found!")
        return None

    @classmethod
    def get_player_code(cls, player_name):
        url = f"https://v3.football.api-sports.io/players?search={player_name}"

        response = requests.get(url, headers=cls.HEADERS)
        if response.ok:
            for player in response.json()["response"]:
                if player["player"]["name"].lower() == player_name.lower():
                    return player["player"]["id"]
        print("Player not found!")
        return None


def main():
    print("Welcome to Soccer Match Filter!")
    while True:
        print("\nMain Menu:")
        print("1. View Matches by Team")
        print("2. View Matches by League")
        print("3. View Matches by Player")
        print("4. Exit")
        choice = input("Please choose an option (1-4): ")

        if choice == "1":
            team_name = input("Enter team name: ")
            team_code = APIFootball.get_team_code(team_name)
            matches = APIFootball.get_matches(team=team_code)
            display_matches(matches)
        elif choice == "2":
            league_name = input("Enter league name: ")
            league_code = APIFootball.get_league_code(league_name)
            matches = APIFootball.get_matches(league=league_code)
            display_matches(matches)
        elif choice == "3":
            player_name = input("Enter player name: ")
            player_code = APIFootball.get_player_code(player_name)
            matches = APIFootball.get_matches(player=player_code)
            display_matches(matches)
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


def display_matches(matches):
    if matches:
        for match in matches:
            print(
                f"{match.team1} vs {match.team2} - {match.date} {match.time} - {match.venue}"
            )
    else:
        print("No matches found!")


if __name__ == "__main__":
    main()


# url = "https://v3.football.api-sports.io/{endpoint}"

# payload={}
# headers = {
#   'x-rapidapi-key': 'XxXxXxXxXxXxXxXxXxXxXxXx',
#   'x-rapidapi-host': 'v3.football.api-sports.io'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
