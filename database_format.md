# Database

## player   
*Save information for players.*
- **id** (int)
ID that auto incresed for player
- **tag** (varchar)
Tag to identify a player in the program
- **event** (varchar)
The player's group *(ex: 30m, 70m)*, use ==event== to prevent confict with SQL keyword ==group==

## stage
*Save rule of stages.*
- **id** (int)
ID that auto incresed for database's usage.
- **name** (varchar)
The name of the stage in program.
- **game_mode** (varchar)
==Qualifying== or ==DualMatch==.
- **total_wave** (int)
How many waves a player should shoot in the **stage**.
- **shots_per_wave** (int)
How many arrows a player should shoot in **one wave**.

## compet
*Match the position for a player(tag) in specific stage.*
- **id** (int)
ID that auto incresed for database's usage.
- **stage** (varchar)
What stage that this match is for.
- **tag** (varchar)
The player in the match.
- **position** (int)
The player's assigned position.

## wave
*Each wave for players in each stage.*
- **id** (int)
ID that auto incresed for database's usage.
- **stage** (varchar)
Which stage this wave is in.
- **tag** (varchar)
The player who generate this wave.
- **position** (int)
Where the wave is generated.
- **shots** (varchar)
The shots, the format is serialized array.
- **score** (int)
The total score of these shots.
- **point** (int)
The point calculated by stage rule.
- **winner** (bool)
In dual match, if this wave makes this player win.
- **timestamp** (timestamp)
Auto generated current timestamp, used for record.

## stage_list
*Save the flow of the whole contest.*
- **id** (int)
ID that auto incresed, a contest will take its stage from lower ID ones, then higher.
- **contest** (varchar)
The contest name, used to classify each stage flow.
- **stage** (varchar)
Stage name from *stage* table.
- **finished** (bool)
If this stage is finished.
