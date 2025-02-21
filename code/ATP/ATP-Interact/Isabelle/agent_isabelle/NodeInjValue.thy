theory NodeInjValue
  imports Main
begin

datatype tree = Leaf | Node tree int tree

lemma Node_inj_value: 
  assumes "Node l1 v1 r1 = Node l2 v2 r2"
  shows "v1 = v2"
proof -
  from assms have "l1 = l2 \<and> v1 = v2 \<and> r1 = r2"
    by (cases "Node l1 v1 r1", cases "Node l2 v2 r2", auto)
  thus ?thesis by simp
qed

end
