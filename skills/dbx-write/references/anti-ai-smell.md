# Anti AI Smell

AI smell is not a list of forbidden words. It is a failure pattern: the text sounds complete before it has earned a judgment.

Use this as a smell detector, not a mechanical replacement script.

## Structural smells

### 1. Smooth but weightless

Symptoms:

- every paragraph is balanced;
- no paragraph risks a stance;
- all conclusions are safely agreeable;
- the writing feels like a summary of what a thoughtful person might say.

Repair:

- sharpen the thesis;
- add a cost or counterexample;
- name who would disagree;
- introduce a concrete scene.

### 2. Topic expansion instead of depth

Symptoms:

- the article keeps adding aspects: technology, organization, individual, future;
- each section is a small generic essay;
- no section changes the original claim.

Repair:

- return to one thesis;
- make each section cut deeper into the same pressure point.

### 3. False symmetry

Symptoms:

```text
A 有好处，也有挑战。
我们既要拥抱变化，也要保持理性。
既不能盲目乐观，也不能过度悲观。
```

Repair:

- name the deciding variable;
- choose a stance under a condition.

### 4. Grand closing mist

Symptoms:

```text
愿我们都能在变化中找到自己的答案。
未来属于那些持续学习、保持开放的人。
```

Repair:

- end with the refined thesis;
- return to the opening scene;
- name the boundary.

### 5. List inflation

Symptoms:

- too many bullets;
- every bullet has similar weight;
- lists replace narrative movement;
- the article feels like slides.

Repair:

- convert the strongest two bullets into prose;
- delete minor bullets;
- add relationships among points.

## Phrase smells

### "不是 A，而是 B"

This can be useful once. Repetition becomes a machine.

Weak:

```text
写作不是表达技巧，而是认知能力。
```

Better:

```text
写作技巧只能改善句子。真正决定文章质量的，是作者有没有一个经得起追问的判断。
```

### "随着 X 的发展"

Weak:

```text
随着 AI 的快速发展，写作方式正在发生变化。
```

Better:

```text
AI 让一篇文章更容易被写出来，也让一篇文章更容易暴露出它其实没有观点。
```

### "这背后反映了"

Weak:

```text
这背后反映了团队协作中的深层问题。
```

Better:

```text
真正的问题是：没有人对状态边界负责。
```

### "值得注意的是"

Usually delete it and say the thing.

### "赋能 / 抓手 / 闭环 / 底层逻辑"

Only keep when:

- the word is a term in the user's context;
- the paragraph defines the mechanism;
- the word is being criticized.

Otherwise replace with concrete process.

## AI-like emotional writing

Weak:

```text
在这个过程中，我们学会了接纳自己，也学会了与世界温柔相处。
```

Better:

```text
我没有突然变得平静。我只是开始承认，有些焦虑不是靠再努力一点就能消失的。
```

## AI-like technical writing

Weak:

```text
前端工程化不仅提升了开发效率，也增强了团队协作能力。
```

Better:

```text
前端工程化真正省下来的，不是敲代码的时间，而是每次改动前确认“会不会炸”的时间。
```

## Repair checklist

Before final output, ask:

- Which sentence could only appear in this article?
- Which paragraph names a real mechanism?
- Which claim has a cost?
- Which example prevents abstraction from floating away?
- Which ending sentence could survive without "总结"?
- What did the article discover that the title did not already say?
