theory AndIntro
  imports Main
begin

lemma and_intro:
  fixes A B :: "bool"
  assumes HA: "A" and HB: "B"
  shows "A \<and> B"
proof -
  from HA and HB show "A \<and> B"
    by (rule conjI)
qed

end
