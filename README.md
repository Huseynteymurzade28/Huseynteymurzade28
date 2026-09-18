<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/line-header-dark.svg">
  <img src="assets/line-header-light.svg" width="100%" alt="Hüseyn Teymurzade — computer engineering @ Marmara University">
</picture>

I write software close to the machine — allocators, interpreters, emulators —
and terminal programs that are pleasant to live in. Mostly Rust, C, Zig and Go,
on Linux.

<p align="center">
  <img src="assets/desk.svg" width="100%" alt="pixel art: a desk at night — string lights, a monitor with code, coffee, a lamp and a cat asleep" />
</p>

```rust
// about.rs

struct Huseyn {
    studies:     &'static str,
    writes:      &'static [&'static str],
    cares_about: &'static [&'static str],
    lives_in:    &'static str,
}

const ME: Huseyn = Huseyn {
    studies:     "computer engineering, marmara university",
    writes:      &["rust", "c", "zig", "go"],
    cares_about: &["memory layouts", "schedulers", "interpreters", "terminals"],
    lives_in:    "a tty, on linux",
};

fn main() {
    println!("{}", ME.studies);
    println!("writes {} · lives in {}", ME.writes.join(", "), ME.lives_in);
    for thing in ME.cares_about {
        // take it apart, see how it works, put it back together
        println!("  {thing}");
    }
}
```

### Toolbox

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=c%2Ccpp%2Crust%2Czig%2Cgo%2Cpython%2Cts%2Clua%2Cbash&theme=dark">
    <img src="https://skillicons.dev/icons?i=c%2Ccpp%2Crust%2Czig%2Cgo%2Cpython%2Cts%2Clua%2Cbash&theme=light" height="48" alt="C, C++, Rust, Zig, Go, Python, TypeScript, Lua, Bash" />
  </picture>
  <br>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=linux%2Cneovim%2Cnix%2Cgit%2Cdocker%2Cpostgres&theme=dark">
    <img src="https://skillicons.dev/icons?i=linux%2Cneovim%2Cnix%2Cgit%2Cdocker%2Cpostgres&theme=light" height="48" alt="Linux, Neovim, Nix, Git, Docker, PostgreSQL" />
  </picture>
</p>

<sub>also Odin · Ratatui · Bubbletea · egui · raylib · SDL2</sub>

### Elsewhere

<p>
  <a href="https://www.linkedin.com/in/hüseyn-teymurzade-9492a92b3"><img src="assets/btn-linkedin.svg" height="33" alt="LinkedIn" /></a>&nbsp;&nbsp;
  <a href="mailto:huseynteymurrr74@gmail.com"><img src="assets/btn-email.svg" height="33" alt="Email" /></a>&nbsp;&nbsp;
  <a href="https://www.leetcode.com/flearlyly"><img src="assets/btn-leetcode.svg" height="33" alt="LeetCode" /></a>&nbsp;&nbsp;
  <a href="https://www.codewars.com/users/Huseyn%20Teymurzade"><img src="assets/btn-codewars.svg" height="33" alt="Codewars" /></a>
</p>

<sub>Most of this runs in a terminal. Most of the rest wishes it did.</sub>
