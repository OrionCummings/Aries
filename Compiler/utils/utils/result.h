#ifndef __RESULT_H
#define __RESULT_H

#ifndef __cplusplus
#  define decltype typeof
#  include <stdbool.h>
#endif
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

/// @cite: https://gist.github.com/LAK132/0d264549745e8196df1e632d5b518c37

#define TOKEN_CONCAT_EX(x, y) x##y
#define TOKEN_CONCAT(x, y)    TOKEN_CONCAT_EX(x, y)
#define UNIQUIFY(x)           TOKEN_CONCAT(x, __LINE__)

#define result_ex(T, E) result_##T##_##E##_t
#define result(T, E)    result_ex(T, E)
#define resultdecl(T, E)                                                      \
  typedef struct                                                              \
  {                                                                           \
    bool _is_ok;                                                              \
    union                                                                     \
    {                                                                         \
      T _ok;                                                                  \
      E _err;                                                                 \
    };                                                                        \
  } result(T, E)

#define ok(V, T, E)                                                           \
  ((result(T, E)){                                                            \
    ._is_ok = true,                                                           \
    ._ok    = V,                                                              \
  })
#define err(V, T, E)                                                          \
  ((result(T, E)){                                                            \
    ._is_ok = false,                                                          \
    ._err   = V,                                                              \
  })

#define is_ok(V)  (V._is_ok)
#define is_err(V) (!(V._is_ok))

#define if_let_ok(I, V)                                                       \
  if (is_ok(V))                                                               \
    for (bool UNIQUIFY(once) = true; UNIQUIFY(once);)                         \
      for (decltype(V._ok) I = V._ok; UNIQUIFY(once); UNIQUIFY(once) = false)
#define if_let_err(I, V)                                                      \
  if (is_err(V))                                                              \
    for (bool UNIQUIFY(once) = true; UNIQUIFY(once);)                         \
      for (decltype(V._err) I = V._err; UNIQUIFY(once); UNIQUIFY(once) = false)

#define unwrap(V)     ((is_ok(V) ? (void)0 : abort()), V._ok)
#define unwrap_err(V) ((is_err(V) ? (void)0 : abort()), V._err)

#define get_ok(V)  (is_ok(V) ? &(V._ok) : nullptr)
#define get_err(V) (is_err(V) ? &(V._err) : nullptr)

#define map(V, T, E, F) (is_ok(V) ? ok(F(V._ok), T, E) : err(V._err, T, E))
#define map_err(V, T, E, F)                                                   \
  (is_err(V) ? ok(V._ok, T, E) : err(F(V._err), T, E))

#define and_then(V, T, E, F) (is_ok(V) ? F(V._ok) : err(V._err, T, E))
#define or_else(V, T, E, F)  (is_ok(V) ? ok(V._ok, T, E) : F(V._err))

#define flatten(V, T, E)                                                      \
  (is_ok(V) ? (is_ok(V._ok) ? ok(V._ok._ok, T, E) : err(V._ok._err, T, E))    \
            : err(V._err, T, E))

/*
typedef struct
{
  int val;
} thing_t;

resultDecl(int, bool);
resultDecl(thing_t, bool);
resultDecl(result(thing_t, bool), bool);

thing_t make_thing(int v)
{
  return (thing_t){.val = v};
}

result(thing_t, bool) maybe_make_thing(int v)
{
  if (v % 200 == 0)
    return err(v == 200, thing_t, bool);
  else
    return ok(make_thing(v), thing_t, bool);
}

result(int, bool) test(bool v, int i)
{
  if (v || i == 0)
    return err(v, int, bool);
  else
    return ok(i, int, bool);
}

int main()
{
  int input1, input2;
  fscanf(stdin, "%d %d", &input1, &input2);

  result(int, bool) result = test(input1 != 20, input2);

  if_let_ok(ok, result) { fprintf(stdout, "%d\n", ok); }
  else if_let_err(err, result)
  {
    fprintf(stderr, "%s\n", err ? "true" : "false");
  }

  result(thing_t, bool) thing = map(result, thing_t, bool, make_thing);

  if_let_ok(ok, thing) { fprintf(stdout, "we got a thing %d\n", ok.val); }

  result(result(thing_t, bool), bool) maybe_thing =
    map(result, result(thing_t, bool), bool, maybe_make_thing);

  result(thing_t, bool) flattened = flatten(maybe_thing, thing_t, bool);

  if_let_ok(ok, flattened)
  {
    fprintf(stdout, "we got a flattened thing %d\n", ok.val);
  }

  result(thing_t, bool) and_thend =
    and_then(result, thing_t, bool, maybe_make_thing);

  if_let_ok(ok, and_thend)
  {
    fprintf(stdout, "we got an and_then'd thing %d\n", ok.val);
  }
}
*/

#endif