theory LogicEx3
  imports Main
begin

lemma logic_ex3:
  fixes P Q :: "'a \<Rightarrow> bool"
  assumes H: "\<forall>a. P a \<longrightarrow> Q a"
  shows "\<forall>a. \<not> Q a \<longrightarrow> \<not> P a"
proof (intro allI impI)
  fix a
  assume "\<not> Q a"
  have "P a \<longrightarrow> Q a" using H by (rule allE)
  show "\<not> P a"
  proof
    assume "P a"
    from `P a \<longrightarrow> Q a` and `P a` have "Q a" by (rule mp)
    from `\<not> Q a` and `Q a` show False by contradiction
  qed
qed

end
