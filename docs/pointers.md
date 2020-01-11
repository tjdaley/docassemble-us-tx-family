---
layout: default
title: Pointers for Interview Development
short_title: Pointers
order: 22
---

## Saving Your Case

In the *functions* module, there is a save_case() function. It takes two arguments: The user's identifier and a reference
to the instance of the *Case* class that you are working with.

You can call *save_case()* at any time and the case will be saved up to that point. There is some chance that the final
question block of the interview will motivate [docasemble] to prompt the user for more information, usually based on the
variables referenced in the template document. You want to make sure those variables are saved, too, if they are part of the case you are working on.

To make sure your case is saved, in full, at the end of each interview, include this code block as the very last part of the interview that is processed:

```
  % if save_case(case):
    Your case has been saved.
  % endif
```

At this time *save_case()* does not return anything other than *NoneType* so you'll never see the "Your case has been saved." message.


[docassemble]: https://docassemble.org
