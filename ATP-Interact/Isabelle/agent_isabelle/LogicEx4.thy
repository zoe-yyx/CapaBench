theory LogicEx4
  imports Main
begin

lemma logic_ex4:
  fixes P Q :: "'a \<Rightarrow> bool"
  assumes H: "\<forall>a. \<not> Q a \<longrightarrow> \<not> P a"
  shows "\<forall>a. P a \<longrightarrow> Q a"
proof (intro allI impI)
  fix a
  assume "P a"
  have "\<not> Q a \<longrightarrow> \<not> P a" using H by (rule allE)
  show "Q a"
  proof (rule ccontr)
    assume "\<not> Q a"
    from `\<not> Q a \<longrightarrow> \<not> P a` and `\<not> Q a` have "\<not> P a" by (rule mp)
    from `P a` and `\<not> P a` show False by contradiction
  qed
qed

end
