theory ReverseSize
  imports Main
begin

datatype tree = Leaf | Node tree int tree

fun tree_reverse :: "tree \<Rightarrow> tree" where
  "tree_reverse Leaf = Leaf"
| "tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

fun tree_size :: "tree \<Rightarrow> int" where
  "tree_size Leaf = 0"
| "tree_size (Node l v r) = tree_size l + tree_size r + 1"

lemma reverse_size: "tree_size (tree_reverse t) = tree_size t"
proof (induct t arbitrary: l v r)
  case Leaf
  then show ?case by simp
next
  case (Node l v r)
  (* Induction hypotheses:
     Node.IH: 
       1. tree_size (tree_reverse l) = tree_size l
       2. tree_size (tree_reverse r) = tree_size r
  *)
  from Node have IHl: "tree_size (tree_reverse l) = tree_size l"
    using Node.IH(1) by simp
  from Node have IHr: "tree_size (tree_reverse r) = tree_size r"
    using Node.IH(2) by simp
  have "tree_size (tree_reverse (Node l v r)) = tree_size (Node (tree_reverse r) v (tree_reverse l))"
    by simp
  also have "... = tree_size (tree_reverse r) + tree_size (tree_reverse l) + 1"
    by simp
  also have "... = tree_size r + tree_size l + 1"
    using IHl IHr by simp
  also have "... = tree_size l + tree_size r + 1"
    by (simp add: add.commute)
  also have "... = tree_size (Node l v r)"
    by simp
  finally show ?case .
qed

end