theory NotEx1
  imports Main
begin

lemma not_ex1: "\<forall>n m::int. n < m \<or> \<not> (n < m)"
proof -
  {
    fix n m :: int
    have "n < m \<or> \<not> (n < m)"
      using classical by auto
  }
  thus ?thesis by auto
qed

end