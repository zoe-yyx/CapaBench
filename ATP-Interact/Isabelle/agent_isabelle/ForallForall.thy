theory ForallForall
  imports Main
begin

theorem forall_forall:
  fixes P :: "'a \<Rightarrow> 'b \<Rightarrow> bool"
  assumes "\<forall>x y. P x y"
  shows "\<forall>y x. P x y"
proof -
  from assms show "\<forall>y x. P x y" 
    by (simp add: assms)
qed

end
