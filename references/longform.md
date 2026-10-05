# Long-form: blog posts, newsletters, essays

Long-form gives AI habits room to compound. A single "Moreover" is invisible, but twelve sections in the same shape, each ending on a lesson, add up to a piece the reader finishes knowing nothing new. Spend most of the effort on structure and specifics.

## How good long-form works

- **The title makes a claim or names a thing.** "We cut our AWS bill 60% by deleting one service" beats "Optimizing Cloud Costs: A Comprehensive Guide."
- **Open with the most interesting thing.** That might be the most interesting specific thing: a number, a scene, a mistake, a claim someone would argue with. Context can come after.
- **Structure follows the material.** If one part is hard, give it most of the words. Don't pad easy sections to match. Five sections of equal length is a tell.
- **Headings name what's under them.** "What we tried first" or "Why the cache made it worse" tells the reader something. "The Challenge" and "Key Takeaways" don't. Use sentence case. Skip headings entirely in pieces under about 800 words unless the reader will scan.
- **Paragraphs vary.** Some run six sentences because the idea needs it. Some are one line. Avoid the claim, elaboration, example, wrap-up template in every paragraph.
- **Prose over bullets for arguments.** Bullets are for lists of parallel things (steps, ingredients, options). Reasons that build on each other belong in sentences connected by "because," "so" and "but."
- **Have a view.** Essays and newsletters exist because a person thinks something. Say it, defend it, admit where you might be wrong once, and move on.
- **Include the mess.** Say what you tried that didn't work and what you still don't know. A model can't generate that, and it's what readers come back for.
- **End on the last real point.** That might be a concrete thing to try, an open question you're still chewing on, or the final piece of the argument. Skip "In conclusion," recaps and inspirational send-offs.

## Tells specific to long-form

| Tell | Looks like | Fix |
|---|---|---|
| Scene-setting opener | "In today's rapidly evolving world of..." "In an era where..." "Have you ever wondered...?" | Delete the first paragraph and see if the second one works as an opener. It usually does |
| Roadmap intro | "In this post, we'll explore X, Y, and Z. Let's dive in!" | Cut. The headings are the roadmap |
| Listicle padding | "7 ways to..." when there are really three good ones | Publish the three |
| Section template | Every section: heading, one-line restatement, three paragraphs, bold takeaway | Vary length and shape. Delete restating first lines |
| Takeaway boxes | "**Key takeaway:**" after every section | Cut. If the section made its point, the reader got it |
| Transition chains | "Now that we've covered X, let's turn to Y." "With that in mind..." | Start the next section with its first real sentence |
| Stock "challenges" section | "Of course, no approach is without its challenges." | Name the specific problem you hit, or cut the section |
| False-balance conclusion | "Ultimately, the right choice depends on your unique needs." | Say what you'd choose and when you'd choose differently |
| Recap ending | Final section restates every heading | End on the last real point |
| Inspirational send-off | "The future is bright for those willing to adapt." "Now go build something amazing." | Cut |
| Newsletter boilerplate | "Hey friends! Hope you're having a great week!" "That's all for this week, see you next time! ✌️" | One line of real greeting is fine if it's your voice. Otherwise start with the first item |

## Examples

### Blog post opening and first section

**Before:**

> # Mastering Database Indexing: A Comprehensive Guide
>
> In the ever-evolving landscape of software development, database performance plays a crucial role in delivering seamless user experiences. Have you ever wondered why some queries take seconds while others return instantly? The answer often lies in indexing.
>
> In this comprehensive guide, we'll delve into the fundamentals of database indexing, explore common pitfalls, and share best practices to help you optimize your queries. Let's get started!
>
> ## Understanding Indexes
>
> Understanding indexes is essential for any developer. An index is a data structure that improves the speed of data retrieval operations...

**Source notes:** Author's team had a dashboard query taking 11 seconds. Cause: an index on (created_at, user_id) when the query filtered by user_id first. Swapping column order brought it to 40ms.

**After:**

> # Swapping two columns in one index took our dashboard from 11 seconds to 40 ms
>
> Our analytics dashboard took 11 seconds to load, even though the query behind it already had an index.
>
> The index was on `(created_at, user_id)`. The query filtered by `user_id` first and then by a date range. Postgres can use a composite index efficiently only when the query filters on the leftmost columns, so it was scanning most of the index anyway. We created the same index with the columns swapped, and the query dropped to 40 milliseconds.
>
> The rest of this post covers how we tracked it down.

The last line is a deliberate signpost. One is fine when the reader needs to know more is coming.

### Newsletter section

**Before:**

> ## 📚 What I'm Reading
>
> This week I dove into "The Mom Test" by Rob Fitzpatrick, and wow — what a game-changer! This book is a must-read for any founder looking to master the art of customer conversations. It offers invaluable insights into asking the right questions and avoiding common pitfalls. Highly recommend!

**Source notes:** Writer's actual reaction: the chapter on compliments being useless data changed how they ran interviews. Before, they'd count "I'd totally use that" as validation.

**After:**

> ## What I'm reading
>
> *The Mom Test* by Rob Fitzpatrick. The chapter that got me is the one about compliments. I'd been counting "oh, I'd totally use that" as a yes in customer interviews. Fitzpatrick's point is that compliments cost the person nothing, so they tell you nothing. Now I ask what they're using today and what it costs them, The conversation is more awkward, and I learn more from it.

### Essay paragraph

**Before:**

> Burnout is not merely a personal failing; it is a systemic issue that reflects broader organizational dynamics. When companies prioritize productivity over wellbeing, they create environments where exhaustion becomes normalized. This underscores the importance of fostering a culture of sustainable work practices.

**After (writer supplied the situation):**

> I burned out in 2022. Nobody overworked me on purpose, which made it harder to see. On-call rotated between four of us, a teammate left in March and nobody replaced him, and by summer I was on call every third week instead of every fourth. Each week was manageable. I can't point to the week it stopped being manageable, and I don't think anyone else could have either.

Without the writer's situation, the best you can do is cut this paragraph down. Ask them what happened.
