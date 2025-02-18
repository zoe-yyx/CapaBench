theory FourIsEven
  imports Main
begin

lemma four_is_even: "\<exists>n. 4 = n + n"
proof -
  have "4 = 2 + 2" by simp
  thus ?thesis by blast
qed

end
