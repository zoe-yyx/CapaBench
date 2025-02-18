theory OrExample
  imports Main
begin

lemma or_example:
  fixes P Q R :: "bool"
  assumes H1: "P \<longrightarrow> R" and H2: "Q \<longrightarrow> R" and H3: "P \<or> Q"
  shows "R"
proof -
  from H3 show "R"
  proof
    assume "P"
    from H1 and `P` show "R" by (rule mp)
  next
    assume "Q"
    from H2 and `Q` show "R" by (rule mp)
  qed
qed

end