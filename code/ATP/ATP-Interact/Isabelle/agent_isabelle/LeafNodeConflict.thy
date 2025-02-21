theory LeafNodeConflict
  imports Main
begin

datatype tree = Leaf | Node tree int tree

lemma Leaf_Node_conflict:
  assumes "Leaf = Node l v r"
  shows "1 = 2"
proof -
  have "Leaf \<noteq> Node l v r" by simp
  with assms have False by contradiction
  thus "1 = 2" by simp
qed

end
