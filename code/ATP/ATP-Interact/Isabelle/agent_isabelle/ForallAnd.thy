theory ForallAnd
  imports Main
begin

theorem forall_and: "(\<forall>a. P a \<and> Q a) = ((\<forall>a. P a) \<and> (\<forall>a. Q a))"
proof -
  {
    assume "\<forall>a. P a \<and> Q a"
    then have "\<forall>a. P a" and "\<forall>a. Q a" by auto
  }
  moreover {
    assume "(\<forall>a. P a)" and "(\<forall>a. Q a)"
    then have "\<forall>a. P a \<and> Q a" by auto
  }
  ultimately show ?thesis by auto
qed

end
