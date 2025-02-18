theory tmp_default
  imports Main
begin

(* 定义单调性 *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* 证明常数函数是单调的 *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof
  fix a
  show "mono (\<lambda>x. a)"
  proof
    fix n m
    assume "n \<le> m"
    then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
      by simp
  qed
qed

(* Define f *)
definition f :: "int \<Rightarrow> int" where "f = (\<lambda>x. a)"

(* Show f is monotonically increasing *)
show "mono f"
proof
  fix n m
  assume "n \<le> m"
  then show "f n \<le> f m"
    by simp
qed

(* Complete the proof *)
(* Show the monotonicity of f *)
show "mono (\<lambda>x. a)"
proof
  fix n m
  assume "n \<le> m"
  then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
    by simp
qed
(* Fix a and show that mono (\<lambda>x. a) *)
fix a
show "mono (\<lambda>x. a)"
proof
  fix n m
  assume "n \<le> m"
  then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
    by simp
qed

(* Define f *)
definition f :: "int \<Rightarrow> int" where "f = (\<lambda>x. a)"

(* Show f is monotonically increasing *)
show "mono f"
proof
  fix n m
  assume "n \<le> m"
  then show "f n \<le> f m"
    by (simp add: f_def)
qed

(* Complete the proof *)
(* Show the monotonicity of f *)
show "mono (\<lambda>x. a)"
proof
  fix n m
  assume "n \<le> m"
  then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
    by simp
qed
(* Fix a and show that mono (\<lambda>x. a) *)
fix a
show "mono (\<lambda>x. a)"
proof
  fix n m
  assume "n \<le> m"
  then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
    by simp
qed
end
