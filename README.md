# What is going on???
For a better way to read the book pages i provided a serialized json file with all the text components. Running the `get_book.py` script will copy to your clipboard the /give command for the book. (make sure you have `pyperclip` installed).

The best way to explain what this does is by analizing each lang compent and what they are used for and with what they translated with
## `"item.smithed.wiki.book.page"`
```json
"item.smithed.wiki.book.page_none": "\ua00d\ua00b\ua00e\ua00c",
"item.smithed.wiki.book.page_previous": "\ua015\ua00b\ua00e\ua00c",
"item.smithed.wiki.book.page_next": "\ua016\ua00b\ua00e\ua00c",
"item.smithed.wiki.book.page_both": "\ua017\ua00b\ua00e\ua00c"
```
This part is what makes the book texture that covers the old one (including arrows), that's why there are 4 separate components:
- `page_none`: no arrows need to be displayed (in the case of an entry with a single page)
- `page_previous`: only the arrow to go to the previous page needs to be displayed
- `page_next`: only the arrow to go to the next page needs to be displayed 
- `page_both`: both arrows need to be displayed
What each char does:
- `\ua00d`, `\ua015`, `\ua016`, `\ua017` are the chars associated to the textures that have or dont have holes that allow for the vanilla buttons to render
- `\ua00b\ua00e\ua00c` make the rest of the book, in specific `\ua00e` is the second part of the book texture that covers the leftmost part of the texture.

## `"item.smithed.wiki.book.recipe"`
This is the string that you use when you want to display a crafting recipe. I will break down the string into multiple lines based on where the `\n`'s are.
- `\n\ua00f\ua009%1$s%3$s%5$s`: `\ua00f` is the main recipe texture, `%1$s`, `%3$s`, `%5$s` are the text compnents associated with each item of the first row.
```json
{
  "translate":"item.smithed.wiki.book.recipe_icon.cool",
  "font":"smithed.wiki:book/recipe_icons",
  "hoverEvent":{
    "action":"show_text",
    "value":[
      {
        "translate":"item.custom.cool",
        "font":"default"
      }
    ]
  }
}
```
This is an example text component with a hover event.
- `\n\ua009%2$s%4$s%6$s`: this row provides the "invisible but equally wide" chars used to make sure that the ones from the line above have click and hover events that are two lines tall (to match the char's height).
```json
{
  "translate":"item.smithed.wiki.book.recipe_icon.transparent",
  "font":"smithed.wiki:book/recipe_icons",
  "hoverEvent":{
    "action":"show_text",
    "value":[
      {
        "translate":"item.custom.cool",
        "font":"default"
      }
    ]
  }
}
```
This is an example text component to use if the item in the first column of the row above has a hover event.
- `\n\ua009%7$s%9$s%11$s\ua00a%19$s%21$s`: This row is the same as the one above except it has two extra slots for text components: one is the output item (has same text component structure as the ingredient ones) and one extra optional for the count (which will be mentioned later but a `""` will suffice if the count is 1).
- `\n\ua009%8$s%10$s%12$s\ua00a%20$s`: exact same structure as the `\n\ua009%2$s%4$s%6$s` line but with the extra slot for the output item hover and click events.
- `\n\ua009%13$s%15$s%17$s`: Same as `\n\ua00f\ua009%1$s%3$s%5$s` (third row crafting ingredients).
- `\n\ua009%14$s%16$s%18$s`: Same as `\n\ua009%2$s%4$s%6$s`: third row crafting ingredients invisible font providers.

## `"item.smithed.wiki.book.recipe_icon.transparent"`
The invisible char with same width as the font of the items with a "container" background, used in crafting recipes, needs to share click and hover events of previous component in the `"with"` array.
## `"item.smithed.wiki.book.recipe_icon.empty"`
Used to display empty containers in the crafting table, doesnt need the invisible char below since they don't have click or hover events.
## `"item.smithed.wiki.book.recipe_output_count_single":"\ua002%s"` and `"item.smithed.wiki.book.recipe_output_count_double":"\ua003%s"`
Used for recipes with count greater then 1
- `count==1`: `""`  
- `2<=count<=9`: `"item.smithed.wiki.book.recipe_output_count_single"`  
- `count>=10`: `"item.smithed.wiki.book.recipe_output_count_double"`

## `"item.smithed.wiki.book.arrows"`
ALWAYS needs to be in line 15 the book, used to block functionality of the regular book arrows (IT'S TWO LINES TALL TO COVER THE BUTTONS COMPLETELY). Here's an example text component:
```json
{
  "translate":"item.smithed.wiki.book.arrows",
  "font":"smithed.wiki:book/main",
  "color":"white",
  "with":[
    {
      "translate":"item.smithed.wiki.book.arrow_blocker",
      "clickEvent":{
        "action":"change_page",
        "value":""
      }
    },
    {
      "translate":"item.smithed.wiki.book.arrow_blocker",
      "clickEvent":{
        "action":"change_page",
        "value":"2"
      }
    }
  ]
}
```
In this case the arrow that goes to the previous page dosen't do anything (`change_page` value is `""`), whereas the second case we have an arrow pointing to page 2.
## `"item.smithed.wiki.book.arrow_blocker"`
Just a spacer used to get the previous text component in the right position.
## `"item.smithed.wiki.book.footer"`
ALWAYS needs to be at line 13 of all non-index pages.  
`\ua006\ua007%s\ua012%s\n`: the first `%s` needs to be a footer icon, here's an example:
```json
{
    "translate":"item.smithed.wiki.book.icon.epic",
    "font":"smithed.wiki:book/footer"
    "color":"white",
}
```
Note that the hover event for this icon needs to be put in the `"item.smithed.wiki.book.footer"` component and not in `"item.smithed.wiki.book.icon.epic"`
The second `%s` is used to display the page numbers, here's an example:
```json
{
    "translate":"item.smithed.wiki.book.page_number",
    "font":"smithed.wiki:book/footer",
    "color":"black",
    "with":[
      1,
      5
    ]
}
```
## `"item.smithed.wiki.book.page_number"`
Formats the page display mentioned above, for now `"%s-%s"`.
## `"item.smithed.wiki.book.index"`
*Oh boy this is going to be tough*  
I will break down the component where the `\n`'s are.
- `\ua000\ua003%s\n`: `\ua000` displays the 6x6 grid and `\ua003` is a negative space wide as much as the grid texture, looking back i dont think it's even useful.
- `\ua001\ua001%s%s%s%s%s%s\n`: This line is used to display the tabs for the various categories `\ua001`offsets the first tab. Each of the subsequent `%s`'s are used for a different category tab, here's an example:
```json
{
  "translate":"item.smithed.wiki.book.index.category.example_selected",
  "color":"white",
  "font":"smithed.wiki:book/main",
  "hoverEvent":{
    "action":"show_text",
    "value":[
      {
        "text":"my funny category"
      }
    ]
  }
}
```
- `\ua014%s\n`: This line is used for the first row of items to display, `%s` is an array that can hold up to 6 items, here's an example item:
```json
{
  "translate":"item.smithed.wiki.book.icon.cool",
  "font":"smithed.wiki:book/index_icons",
  "hoverEvent":{
    "action":"show_text",
    "value":[
      {
        "translate":"item.custom.cool"
      }
    ]
  }
}
```
- `\ua014%s\n`: Just like with crafting recipes, we need to make the hover and click events 2 lines tall to match the icon height. Just like in the line before `%s` is an array that can hold up to 6 items, but the items are invisible and have same click and hover events as the one directly above blah blah I already explained this in the crafting part. Here's an example component for the item used in the line above:
```json
{
  "translate":"item.smithed.wiki.book.index_space",
  "font":"smithed.wiki:book/index_icons",
  "hoverEvent":{
    "action":"show_text",
    "value":[
      {
        "translate":"item.custom.cool"
      }
    ]
  }
}
```
-`\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n\ua014%s\n%s`: same thing as i just explained for lines 2-6.

## `"item.smithed.wiki.book.index_space"`
Used in the index to make invisible chars as wide as the one above them (assuming they are all 16px wide)
## `"item.smithed.wiki.book.index.category.example"`
`"\ua004\ua001"`: The first one is the texture for an example tab [needs to be made by a player], the second one is a space.

## `"item.smithed.wiki.book.index.category.example_selected"`:
`"\ua005\ua001"`: The first one is the texture for a selected example tab [needs to be made by a player](one pixel deeper then the example one to cover the green outline), the second one is a space.

## Ending words.
What I said here doesn't mention the way the pngs need to be created and the dimensions, I'll briefly explain it here:  
The pngs that are pack added entries that will have their own pages need to be used in 2 fonts: `footer.json` and `index_icons.json` (due to their different vertical offset). If this png also has a crafting recipe that is displayed it also has to be used in recipe icons. But since recipe icons 17x17 the png needs to be applied onto an empty container png (see `assets\smithed.wiki\textures\gui\book\icons\recipe\empty.png` on the non-outline part). This same process needs to be applied to vanilla item textures to make them 17 chars wide. 

## Stuff for the far future
- Converter from 3d model to 2d isometric texture
- Make Indexes