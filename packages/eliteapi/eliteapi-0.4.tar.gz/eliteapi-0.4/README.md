# eliteapi

eliteapi is a Python wrapper for Elite Creative allowing you to easly interact with the API.

## Installation
To install **eliteapi**, run the following command into your terminal:

```
pip install eliteapi
```

## Example Usage

```py
from eliteapi import EliteCreative

elite = EliteCreative('api-key')  # Generate your API key at https://elitescrims.xyz/developer

stats = elite.get_user_stats('user-id')
print(stats)
```

## Methods

* [get_user_stats(user_id)](#get_user_statsuser_id) - Return the users Elite Creative statistics
* [get_user_queue(user_id)](#get_user_queueuser_id) - Returns information about the users queue (if they're queuing)
* [in_game(user_id)](#in_gameuser_id) - Whether or not the user is in an on going match
* [get_match_by_game_id(game_id)](#get_match_by_game_idgame_id) - Get a games statistics by it's game Id
* [get_match_by_user_id(user_id)](#get_match_by_user_iduser_id) - Get a games statistics by one of the players (either player 1 or 2)
* [get_team_by_team_id(team_id)](#get_team_by_team_idteam_id) - Return information about a team by it's Id
* [get_team_by_user_id(user_id)](#get_team_by_user_iduser_id) - Return information about a team by either the captain or member's Id

## get_user_stats(user_id)
Return the users Elite Creative statistics
```py
elite.get_user_stats('user-id')
```

## get_user_queue(user_id)
Returns information about the users queue (if they're queuing)
```py
elite.get_user_queue('user-id')
```

## in_game(user_id)
Whether or not the user is in an on going match
```py
elite.in_game('user-id')
```

## get_match_by_game_id(game_id)
Get a games statistics by it's game Id
```py
elite.get_match_by_game_id('game-id')
```

## get_match_by_user_id(user_id)
Get a games statistics by one of the players (either player 1 or 2)
```py
elite.get_match_by_user_id('user_id')
```

## get_team_by_team_id(team_id)
Return information about a team by it's Id
```py
elite.get_team_by_team_id('team-id')
```

## get_team_by_user_id(user_id)
Return information about a team by either the captain or member's Id
```py
elite.get_team_by_user_id('user-id')
```
