theory NotEx2
  imports Main
begin

lemma not_ex2: "\<forall>P Q. P \<longrightarrow> (\<not> P) \<longrightarrow> Q"
proof -
  {
    fix P Q
    assume a1: "P"
    assume a2: "\<not> P"
    have "False" using a1 a2 by auto
    then have "Q" by blast
  }
  thus ?thesis by blast
qed

end