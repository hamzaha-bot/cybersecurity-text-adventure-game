# Cybersecurity Attack Text Adventure Game - Storyboard

## Game Theme

The game is a cybersecurity-themed text adventure in which the player takes the role of a cybersecurity analyst responding to a ransomware attack.

A Ransomware Bot has taken control of the company's systems. The player must navigate through the building and collect six cybersecurity tools before entering the Control Room.

If the player enters the Control Room before collecting all six tools, the ransomware attack succeeds. If all six tools are collected first, the player can stop the Ransomware Bot and win the game.

## Objective

Collect all six cybersecurity tools:

- MFA Token
- Firewall Key
- Security Patch
- Backup Drive
- Encryption Key
- Access Card

After collecting all six items, enter the Control Room to stop the Ransomware Bot.

## Rooms and Items

| Room | Item / Role |
| --- | --- |
| Main Lobby | Starting Room |
| Security Office | MFA Token |
| Network Operations Center | Firewall Key |
| IT Office | Security Patch |
| Server Room | Backup Drive |
| Data Center | Encryption Key |
| Admin Office | Access Card |
| Control Room | Ransomware Bot |

## Room Connections

### Main Lobby
- West -> Security Office
- North -> Control Room

### Security Office
- East -> Main Lobby
- North -> Network Operations Center

### Network Operations Center
- South -> Security Office
- North -> IT Office

### IT Office
- South -> Network Operations Center
- East -> Server Room

### Server Room
- West -> IT Office
- East -> Data Center

### Data Center
- West -> Server Room
- South -> Admin Office

### Admin Office
- North -> Data Center
- West -> Control Room

### Control Room
- South -> Main Lobby
- East -> Admin Office

## Winning Path

One valid winning route is:

1. Start in the Main Lobby
2. Go west to the Security Office and collect the MFA Token
3. Go north to the Network Operations Center and collect the Firewall Key
4. Go north to the IT Office and collect the Security Patch
5. Go east to the Server Room and collect the Backup Drive
6. Go east to the Data Center and collect the Encryption Key
7. Go south to the Admin Office and collect the Access Card
8. Go west to the Control Room

At this point, the player has all six tools and wins the game.

## Losing Condition

The player loses if they enter the Control Room before collecting all six cybersecurity tools.

## Player Commands

Movement commands:

- `go north`
- `go south`
- `go east`
- `go west`

Item command:

- `get <item name>`

Example:

`get MFA Token`

## Design Goal

The game was designed to combine a cybersecurity storyline with beginner Python programming concepts such as room navigation, inventory management, input validation, decision branching, loops, functions, and dictionaries.