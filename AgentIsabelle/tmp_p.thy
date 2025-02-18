theory ForallEx1
  imports Main
begin

lemma forall_ex1:
  assumes "\<And>x. P x \<longrightarrow> Q x \<longrightarrow> R x"
  shows "\<And>x. P x \<and> Q x \<longrightarrow> R x"
proof -
  fix x
  assume "P x \<and> Q x"
  then have "P x" and "Q x" by (rule conjE)
  have "P x \<longrightarrow> Q x \<longrightarrow> R x" by fact
  then have "P x" using `P x` by (rule modus_ponens)
  then have "Q x" using `P x` `Q x` by (rule modus_ponens)
  then have "R x" using `P x` `Q x` by (rule assms)
  then show "P x \<and> Q x \<longrightarrow> R x" by (rule impI)
  have "P x \<and> Q x \<longrightarrow> R x" using `P x` `Q x` `R x` by (rule modus_ponens)
  then show ?thesis by (rule impI)
qed
end
