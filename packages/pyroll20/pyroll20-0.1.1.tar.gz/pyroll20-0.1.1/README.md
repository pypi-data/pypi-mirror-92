
# PyRoll20

A Roll20 syntax compatible dice roller. 

### Usage Example

```python
import pyroll20

print(pyroll20.roll(user_input="2d20"))

>> [12,8]
```
or with a modifier
```python
import pyroll20

print(pyroll20.roll(user_input="2d20+5"))

>> 23 
```
### Installing
```bash
pip3 install pyroll20
```
### Modifiers
   **'h'** # Highest Rolls - **5d20h3** returns the 3 highest rolls from the five d20 that were rolled.<br/>
    **'l'** # Lowest Rolls - **5d20l3** returns the 3 lowest rolls from the five d20 that were rolled.<br/>
    **'+'**  # Adds to sum - **5d20+3** adds 3 to the sum of the five d20 that were rolled, always returns a single integer.<br/>
    **'-'**  # Subtracts from sum - **5d20-3** subtracts 3 from the sum of the five d20 that were rolled, always returns a single integer.<br/>
    **'t'**  # Sum of all rolls - **5d20t** returns the sum of the five d20 that were rolled.<br/>
    **'e'**  # "Exploding dice - **5d20e** if any of the five rolls goes critical, it gets re-rolled and added to the individual roll. <br/>
## Notes
If sides are provided but no roll number, the roll number defaults to 1, for example **d20** is a valid input.



## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE v3.



