theory ForallForall
  imports Main
begin

theorem forall_forall:
  fixes P :: "'a \<Rightarrow> 'b \<Rightarrow> bool"
  assumes "\<forall>x y. P x y"
  shows "\<forall>y x. P x y"
proof -
  {
    fix y x
    have "P x y" using assms by blast
  }
  thus "\<forall>y x. P x y" by blast
qed

end
