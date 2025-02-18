
assert (C + R = 35) by trivial.
rewrite -> H in "2 * C + 4 * R = 94".
rewrite Zplus_comm with (a := 2 * C) (b := 4 * R) in "2 * C + 4 * R = 94".
rewrite Zmult_comm with (a := 2) (b := C) in "2 * C + 4 * R = 94".
rewrite Zmult_comm with (a := 4) (b := R) in "2 * C + 4 * R = 94".
rewrite Zplus_assoc with (a := 2 * C) (b := 4 * R) (c := 35) in "2 * C + 4 * R = 94".
rewrite Zplus_assoc with (a := 70) (b := 2 * R) (c := 24) in "2 * C + 4 * R = 94".
rewrite Zplus_comm with (a := 70) (b := 24) in "2 * C + 4 * R = 94".
rewrite Zplus_zero_l in "2 * C + 4 * R = 94".
rewrite Zmult_zero_l with (a := 2) in "2 * C + 4 * R = 94".
rewrite Zmult_zero_l with (a := 4) in "2 * C + 4 * R = 94".
rewrite Zplus_zero_l in "2 * C + 4 * R = 94".
rewrite Zmult_zero_l with (a := 2) in "2 * C + 4 * R = 94".
rewrite Zmult_zero_l with (a := 4) in "2 * C + 4 * R = 94".
