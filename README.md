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


Lists all marks that have been set, allowing you to jump to a marked view.

Choose `TakeMeHome: list marks` from the command palette to run.

```json
{ "command": "take_me_home", "args": { "action": "list"} }
```

### Reorder selected

By changing the order of view names listed in the input box, you can change the order of marks and hence their quick jump indexes.
You can also delete marks by removing them from the list in the input box.

For example, given the following list of marks to reorder:

> README.md,actions/list_marks_action.py

if we wanted `list_marks_action.py` to be the first quick jump index we could edit it to:

> actions/list_marks_action.py,README.md

If instead we wanted to delete `README.md` we could edit it to:

> list_marks_action.py

This is similar to opening the `README.md` view and selecting [Unmark File](#unmark).

We could also chose to delete all view names, in which case all the marked views will be cleared. This is similar to [Clearing Marks](#clearing-marks)

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
