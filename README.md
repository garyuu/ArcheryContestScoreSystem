# Archery Contest Score System 

## Introduction

This system is used to score and management an *archery contest*.
Combination with wireless scoring machine.

## Feature

- It can handle both **qualifying** and **dual match**, and flexible for rules.
- Both **team** and **single player** can be accepted for a unit, a team's score can also be automatically calculated.
- Be able to handle a chain of different stages.
- From a qualifying to dual match, it can help automatically ranking.
- After ranking, it also generate the matching for next dual match round.
- Be able to handle the communication with scoring machines.

## Installation

First, ensure your environment has ==Python3== and ==Git==. If no, search them with your OS to figure out how to install them.

Next, if you have not installed the ==pymysql== module, use ==pip== to install it. Commonly you can do it by this command:
`pip install pymysql`
If this do not take effect, you may try search it online to solve this problem.

Finally, at any directory as you wish clone this repo by the command:
`git clone https://github.com/garyuu/ArcheryContestScoreSystem`

## How to Use

Switch to the directory you cloned this repo and simply use one of these command(at least one will work, I think):
`python3 console.py` or `python console.py` or `py console.py`

## Technique

- Python3
    - pymysql (module)

