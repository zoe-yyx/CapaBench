theory ForallIff
  imports Main
begin

theorem forall_iff:
  fixes P Q :: "'a \<Rightarrow> bool"
  assumes "\<forall>x. P x \<longleftrightarrow> Q x"
  shows "(\<forall>x. P x) \<longleftrightarrow> (\<forall>x. Q x)"
proof
  -- "First, show (\<forall>x. P x) \<Longrightarrow> (\<forall>x. Q x)"
  assume "\<forall>x. P x"
  show "\<forall>x. Q x"
  proof
    fix x
    from assms have "P x \<longleftrightarrow> Q x" by auto
    with \<open>\<forall>x. P x\<close> show "Q x" by auto
  qed
next
  -- "Now, show (\<forall>x. Q x) \<Longrightarrow> (\<forall>x. P x)"
  assume "\<forall>x. Q x"
  show "\<forall>x. P x"
  proof
    fix x
    from assms have "P x \<longleftrightarrow> Q x" by auto
    with \<open>\<forall>x. Q x\<close> show "P x" by auto
  qed
qed

end
