theory OrIntror
  imports Main
begin


lemma or_intror:
  fixes A B :: "bool"
  assumes H: "B"
  shows "A \<or> B"
proof -
  show "A \<or> B" using H by (rule disjI2)
qed

end