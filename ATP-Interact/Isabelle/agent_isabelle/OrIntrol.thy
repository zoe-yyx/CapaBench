theory OrIntrol
  imports Main
begin


lemma or_introl:
  fixes A B :: "bool"
  assumes H: "A"
  shows "A \<or> B"
proof -
  show "A \<or> B" using H by (rule disjI1)
qed

end