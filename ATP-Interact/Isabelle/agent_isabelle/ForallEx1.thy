theory ForallEx1
  imports Main
begin

lemma forall_ex1:
  assumes "\<And>x. P x \<longrightarrow> Q x \<longrightarrow> R x"
  shows "\<And>x. P x \<and> Q x \<longrightarrow> R x"
proof
  fix x
  assume conj: "P x \<and> Q x"
  then have px: "P x" by simp
  from conj have qx: "Q x" by simp
  from assms have impl: "P x \<longrightarrow> Q x \<longrightarrow> R x" by simp
  from px qx impl show "R x" by simp
qed

end
