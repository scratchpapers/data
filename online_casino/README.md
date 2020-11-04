## ONLINE CASINO A/B TESTING DATA ANALYSIS USING MYSQL, TABLEAU AND POWERPOINT

### Context: We ran a CRM Casino promo on a selected target of our Casino customers on January 21st and would like to assess the impact of this promo

#### Column Fields & Description

|   FIELD    |    DESCRIPTION    |
| -----------|-------------------|
|  Playerid  |   Unique identifier for customer |
|  Handle    |   Amount wagered per session  |
|  GGR       | Gross Revenue. Formula: Stake - Winning (+ if customer lost, - if customer won)|
|Last_12months_segment| Value tier (based on last 12 months' activity)|
| Target_CG | Target / Control Group|
| Bonus | Bonus Awarded (VIP got $50, High $20, Medium $10 and Low $5) |
| Dated | Date of playing activity |

* Bonus awarded is just one for each customer

### Raw Data Sample in MySQL

![Casino Raw Image](casino_raw.PNG)




