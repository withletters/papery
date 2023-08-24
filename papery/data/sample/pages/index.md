# My web site

Welecome to my web site with [papery](http://github.com/withletters/papery)

:smile: :heart: :thumbsup:

## A Happy Post

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

## Table

| Header 1 | *Header* 2 |
| -------- | -------- |
| `Cell 1` | [Cell 2](http://example.com) link |
| Cell 3 | **Cell 4** |


## Code block

Text

``` text
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

Python

``` python
def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x - 1)
```

## Permalink

### Permalink h3

#### Permalink h4

##### Permalink h5

###### Permalink h6

Hovering header title, a permalink symbol `¶` is appear.

### CSS

The permalink symbol is classified as `headerlink`. For better apperances, apply the CSS like below.

``` css
.headerlink {
  color: gray;
  cursor: pointer;
  padding: 0px 5px;
  text-decoration: none;
  visibility: hidden;
}

.headerlink:hover {
  color: blue;
}

h1:hover .headerlink {
  visibility: visible;
}

h2:hover .headerlink {
  visibility: visible;
}

h3:hover .headerlink {
  visibility: visible;
}

...

```

## Markdown in HTML

<details markdown="block">
<summary> How to use </summary>

#### Markdown text

- A *Markdown* text
- Here is a example with `details` element

``` html
<details markdown="block">
<summary> Example </summary>

#### Example

Something Markdown text...

</details>
```

</details>

### My Favorite Fruits
