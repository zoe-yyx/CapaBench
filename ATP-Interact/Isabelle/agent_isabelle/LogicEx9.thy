theory LogicEx9
  imports Main
begin

lemma logic_ex9:
  fixes P Q :: "'a \<Rightarrow> 'b \<Rightarrow> bool"
  assumes H: "\<forall>a b. \<not> P a b \<or> Q a b"
  shows "\<forall>a b. P a b \<longrightarrow> Q a b"
proof -
  {
    fix a b
    assume "P a b"
    with H have "\<not> P a b \<or> Q a b" by auto
    then have "Q a b" by auto
  }
  thus ?thesis by auto
qed

end

