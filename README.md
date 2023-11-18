# TakeMeHome

[Sublime Text](https://www.sublimetext.com/) plugin that takes you back to your most important files

![]()

## Installation

- Open the command palette with `CMD + SHIFT + P`
- Select `Package Control: Add Repository`
- Enter https://github.com/ssanj/TakeMeHome for the repository
- Select `Package Control: Install Package`
- Choose TakeMeHome


## Functionality

Allows you to mark a set of files that you need to frequently return to. This is useful if you have a few primary files
you are working on but have to open a lot of related but temporary files. The sheer number of files open can make it
difficult to return to the files you really care about. `TakeMeHome` lets you `mark` and `jump` back to those files with ease.

[![TakeMeHome in Action](TakeMeHome.png)](TakeMeHome.mp4)

### Mark

Sets a mark on a view, so that you can jump to it easily when required.

Choose `TakeMeHome: mark file` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "mark"} }
```

### Unmark

Removes a set mark on a view.

Choose `TakeMeHome: unmark file` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "unmark"} }
```

### Listing marks

#### Open selected

Lists all marks that have been set, allowing you to jump to a marked view.

Choose `TakeMeHome: list marks` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "list"} }
```

#### Remove selected
If you press `SHIFT` when selecting a mark, you will be prompted whether to remove the mark from the list.

### Clearing marks

Clears an marks that have been set.

Choose `TakeMeHome: clear marks` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "clear"} }
```

### Close all but marks

Closes all unmarked views. This is useful when you are done researching all related files and just want to work on the
main files you care about.

Choose `TakeMeHome: close unmarked` from the command palette to run.

```json
{ "command":"take_me_home", "args": { "action": "close_unmarked"} }
```

### Quick jumps

Allows you to jump to a marked view based on its marked index. Two indexes are defined, but you can define more and map them to shortcuts.

### Marked index 1:

Choose `TakeMeHome: quick jump - 1` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "quick_jump", "index": 1} }
```

### Marked index 2:

Choose `TakeMeHome: quick jump - 2` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "quick_jump", "index": 2} }
```

## Settings


```
{
  // Whether to turn on debug logging
  "debug": true
}
```
