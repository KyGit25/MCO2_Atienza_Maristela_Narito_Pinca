from pyswip import Prolog

class FamilyRelationshipChatbot:
    """
    A conversational chatbot that understands family relationships using Prolog inference.
    Follows the exact specifications for family relationship statements and questions.
    """
    
    def __init__(self, knowledge_base_file):
        """
        Initialize the chatbot with a Prolog knowledge base.
        
        Args:
            knowledge_base_file (str): Path to the Prolog knowledge base file
        """
        self.prolog_engine = Prolog()
        self.prolog_engine.consult(knowledge_base_file)

    def _extract_names_from_statement(self, statement, relationship_phrase):
        """
        Extract two names from a relationship statement.
        
        Args:
            statement (str): The input statement
            relationship_phrase (str): The relationship phrase to split on
            
        Returns:
            tuple: Two names extracted from the statement
        """
        parts = statement.split(relationship_phrase)
        first_name = parts[0].strip().rstrip('.').lower().capitalize()
        second_name = parts[1].strip().rstrip('.').lower().capitalize()
        return first_name, second_name

    def _is_fact_provable(self, fact_query):
        """
        Check if a fact can be proven from the current knowledge base.
        
        Args:
            fact_query (str): Prolog query to check
            
        Returns:
            bool: True if the fact is provable, False otherwise
        """
        try:
            results = list(self.prolog_engine.query(fact_query))
            return bool(results)
        except Exception:
            return False

    def _has_gender_conflict(self, person_name, expected_gender):
        """
        Check if assigning a gender to a person conflicts with existing knowledge.
        
        Args:
            person_name (str): Name of the person
            expected_gender (str): Gender to check ('male' or 'female')
            
        Returns:
            bool: True if there's a conflict, False otherwise
        """
        opposite_gender = 'female' if expected_gender == 'male' else 'male'
        return self._is_fact_provable(f"{opposite_gender}({person_name.lower()})")

    def _are_persons_related(self, person1, person2):
        """
        Check if two persons are already related in the knowledge base.
        
        Args:
            person1 (str): First person's name
            person2 (str): Second person's name
            
        Returns:
            bool: True if they are related, False otherwise
        """
        return self._is_fact_provable(f"related({person1.lower()}, {person2.lower()})")

    def _would_create_circular_relationship(self, child, parent):
        """
        Check if a parent-child relationship would create circular dependency.
        
        Args:
            child (str): Child's name
            parent (str): Parent's name
            
        Returns:
            bool: True if it would create circular relationship, False otherwise
        """
        # Check if parent is already a descendant of child
        return self._are_persons_related(parent, child)

    def _would_create_invalid_parent_child_relationship(self, child, parent):
        """
        Check if a parent-child relationship would create logical inconsistencies.
        This is more specific than circular relationship check - it allows consistent
        assertions but prevents true logical conflicts.
        
        Args:
            child (str): Child's name
            parent (str): Parent's name
            
        Returns:
            bool: True if it would create invalid relationship, False otherwise
        """
        # Check if child is already a parent/ancestor of the proposed parent
        is_child_ancestor_of_parent = (
            self._is_fact_provable(f"parent({child.lower()}, {parent.lower()})") or
            self._is_fact_provable(f"grandparent({child.lower()}, {parent.lower()})")
        )
        
        # If the parent-child relationship already exists, it's consistent
        existing_relationship = self._is_fact_provable(f"parent({parent.lower()}, {child.lower()})")
        
        # Only invalid if child is ancestor of parent (and they're not already parent-child)
        return is_child_ancestor_of_parent and not existing_relationship

    def _would_create_invalid_sibling_relationship(self, person1, person2):
        """
        Check if a sibling relationship would create logical inconsistencies.
        For siblings, we only check for direct ancestor-descendant relationships,
        not general relatedness (since siblings can be related in other ways).
        
        Args:
            person1 (str): First person's name
            person2 (str): Second person's name
            
        Returns:
            bool: True if it would create invalid relationship, False otherwise
        """
        # Check if one is an ancestor/descendant of the other
        is_parent_child = (self._is_fact_provable(f"parent({person1.lower()}, {person2.lower()})") or
                          self._is_fact_provable(f"parent({person2.lower()}, {person1.lower()})"))
        
        # Check if one is a grandparent/grandchild of the other  
        is_grandparent_grandchild = (self._is_fact_provable(f"grandparent({person1.lower()}, {person2.lower()})") or
                                   self._is_fact_provable(f"grandparent({person2.lower()}, {person1.lower()})"))
        
        return is_parent_child or is_grandparent_grandchild

    def _validate_multiple_children_statement(self, children_list, parent_name):
        """
        Validate that multiple children can be children of the given parent.
        
        Args:
            children_list (list): List of children names
            parent_name (str): Parent's name
            
        Returns:
            bool: True if valid, False if conflicts exist
        """
        for child in children_list:
            if (child.lower() == parent_name.lower() or 
                self._would_create_circular_relationship(child, parent_name)):
                return False
        return True

    def process_statement(self, user_statement):
        """
        Process a user statement and update the knowledge base if valid.
        
        Args:
            user_statement (str): The statement provided by the user
        """
        statement = user_statement.strip()
        
        try:
            # Handle sibling relationships - exact pattern: "[Name] and [Name] are siblings"
            if " and " in statement and " are siblings" in statement:
                self._process_siblings_statement(statement)
            
            # Handle parent relationships - exact pattern: "[Name] and [Name] are the parents of [Name]"
            elif " and " in statement and " are the parents of " in statement:
                self._process_parents_statement(statement)
            
            # Handle multiple children - pattern: "[Name], [Name] and [Name] are children of [Name]"
            elif " are children of " in statement:
                self._process_multiple_children_statement(statement)
            
            # Handle father relationship - exact pattern: "[Name] is the father of [Name]"
            elif " is the father of " in statement:
                self._process_father_statement(statement)
            
            # Handle mother relationship - exact pattern: "[Name] is the mother of [Name]"
            elif " is the mother of " in statement:
                self._process_mother_statement(statement)
            
            # Handle brother relationship - exact pattern: "[Name] is a brother of [Name]"
            elif " is a brother of " in statement:
                self._process_brother_statement(statement)
            
            # Handle sister relationship - exact pattern: "[Name] is a sister of [Name]"
            elif " is a sister of " in statement:
                self._process_sister_statement(statement)
            
            # Handle grandmother relationship - exact pattern: "[Name] is a grandmother of [Name]"
            elif " is a grandmother of " in statement:
                self._process_grandmother_statement(statement)
            
            # Handle grandfather relationship - exact pattern: "[Name] is a grandfather of [Name]"
            elif " is a grandfather of " in statement:
                self._process_grandfather_statement(statement)
            
            # Handle child relationship - exact pattern: "[Name] is a child of [Name]"
            elif " is a child of " in statement:
                self._process_child_statement(statement)
            
            # Handle daughter relationship - exact pattern: "[Name] is a daughter of [Name]"
            elif " is a daughter of " in statement:
                self._process_daughter_statement(statement)
            
            # Handle son relationship - exact pattern: "[Name] is a son of [Name]"
            elif " is a son of " in statement:
                self._process_son_statement(statement)
            
            # Handle aunt relationship - exact pattern: "[Name] is an aunt of [Name]"
            elif " is an aunt of " in statement:
                self._process_aunt_statement(statement)
            
            # Handle uncle relationship - exact pattern: "[Name] is an uncle of [Name]"
            elif " is an uncle of " in statement:
                self._process_uncle_statement(statement)
            
            else:
                print("Invalid statement. Please follow the sentence patterns.")
                
        except Exception:
            print("That's impossible!")

    def _process_siblings_statement(self, statement):
        """Process '[Name] and [Name] are siblings' statement."""
        parts = statement.replace(" are siblings", "").split(" and ")
        if len(parts) == 2:
            person1 = parts[0].strip().rstrip('.').lower().capitalize()
            person2 = parts[1].strip().rstrip('.').lower().capitalize()
            
            if person1.lower() == person2.lower():
                print("That's impossible!")
                return
                
            if self._would_create_invalid_sibling_relationship(person1, person2):
                print("That's impossible!")
                return
                
            self.prolog_engine.assertz(f"sibling({person1.lower()}, {person2.lower()})")
            self.prolog_engine.assertz(f"sibling({person2.lower()}, {person1.lower()})")
            print("OK! I learned something.")
        else:
            print("Invalid statement. Please follow the sentence patterns.")

    def _process_parents_statement(self, statement):
        """Process '[Name] and [Name] are the parents of [Name]' statement."""
        modified_statement = statement.replace(" are the parents of ", " and ")
        parts = modified_statement.split(" and ")
        
        if len(parts) == 3:
            parent1 = parts[0].strip().rstrip('.').lower().capitalize()
            parent2 = parts[1].strip().rstrip('.').lower().capitalize()
            child = parts[2].strip().rstrip('.').lower().capitalize()
            
            # Validation checks
            if (child.lower() == parent1.lower() or child.lower() == parent2.lower() or
                self._would_create_circular_relationship(child, parent1) or
                self._would_create_circular_relationship(child, parent2)):
                print("That's impossible!")
                return
                
            self.prolog_engine.assertz(f"parent({parent1.lower()}, {child.lower()})")
            self.prolog_engine.assertz(f"parent({parent2.lower()}, {child.lower()})")
            print("OK! I learned something.")
        else:
            print("Invalid statement. Please follow the sentence patterns.")

    def _process_multiple_children_statement(self, statement):
        """Process '[Name], [Name] and [Name] are children of [Name]' statement."""
        parts = statement.replace(" are children of ", " and ").replace(", ", " and ").split(" and ")
        
        if len(parts) >= 2:
            children = [child.strip().rstrip('.').lower().capitalize() for child in parts[:-1]]
            parent = parts[-1].strip().rstrip('.').lower().capitalize()
            
            if not self._validate_multiple_children_statement(children, parent):
                print("That's impossible!")
                return
                
            for child in children:
                self.prolog_engine.assertz(f"parent({parent.lower()}, {child.lower()})")
            print("OK! I learned something.")
        else:
            print("Invalid statement. Please follow the sentence patterns.")

    def _process_father_statement(self, statement):
        """Process '[Name] is the father of [Name]' statement."""
        father, child = self._extract_names_from_statement(statement, " is the father of ")
        
        if (father.lower() == child.lower() or
            self._has_gender_conflict(father, 'male') or
            self._would_create_circular_relationship(child, father)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"male({father.lower()})")
        self.prolog_engine.assertz(f"parent({father.lower()}, {child.lower()})")
        print("OK! I learned something.")

    def _process_mother_statement(self, statement):
        """Process '[Name] is the mother of [Name]' statement."""
        mother, child = self._extract_names_from_statement(statement, " is the mother of ")
        
        if (mother.lower() == child.lower() or
            self._has_gender_conflict(mother, 'female') or
            self._would_create_circular_relationship(child, mother)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"female({mother.lower()})")
        self.prolog_engine.assertz(f"parent({mother.lower()}, {child.lower()})")
        print("OK! I learned something.")

    def _process_brother_statement(self, statement):
        """Process '[Name] is a brother of [Name]' statement."""
        brother, sibling = self._extract_names_from_statement(statement, " is a brother of ")
        
        if (brother.lower() == sibling.lower() or
            self._has_gender_conflict(brother, 'male') or
            self._would_create_invalid_sibling_relationship(brother, sibling)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"male({brother.lower()})")
        self.prolog_engine.assertz(f"sibling({brother.lower()}, {sibling.lower()})")
        self.prolog_engine.assertz(f"sibling({sibling.lower()}, {brother.lower()})")
        print("OK! I learned something.")

    def _process_sister_statement(self, statement):
        """Process '[Name] is a sister of [Name]' statement."""
        sister, sibling = self._extract_names_from_statement(statement, " is a sister of ")
        
        if (sister.lower() == sibling.lower() or
            self._has_gender_conflict(sister, 'female') or
            self._would_create_invalid_sibling_relationship(sister, sibling)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"female({sister.lower()})")
        self.prolog_engine.assertz(f"sibling({sister.lower()}, {sibling.lower()})")
        self.prolog_engine.assertz(f"sibling({sibling.lower()}, {sister.lower()})")
        print("OK! I learned something.")

    def _process_grandmother_statement(self, statement):
        """Process '[Name] is a grandmother of [Name]' statement."""
        grandmother, grandchild = self._extract_names_from_statement(statement, " is a grandmother of ")
        
        if (grandmother.lower() == grandchild.lower() or
            self._has_gender_conflict(grandmother, 'female') or
            self._would_create_circular_relationship(grandchild, grandmother)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"female({grandmother.lower()})")
        self.prolog_engine.assertz(f"grandparent({grandmother.lower()}, {grandchild.lower()})")
        print("OK! I learned something.")

    def _process_grandfather_statement(self, statement):
        """Process '[Name] is a grandfather of [Name]' statement."""
        grandfather, grandchild = self._extract_names_from_statement(statement, " is a grandfather of ")
        
        if (grandfather.lower() == grandchild.lower() or
            self._has_gender_conflict(grandfather, 'male') or
            self._would_create_circular_relationship(grandchild, grandfather)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"male({grandfather.lower()})")
        self.prolog_engine.assertz(f"grandparent({grandfather.lower()}, {grandchild.lower()})")
        print("OK! I learned something.")

    def _process_child_statement(self, statement):
        """Process '[Name] is a child of [Name]' statement."""
        child, parent = self._extract_names_from_statement(statement, " is a child of ")
        
        if (child.lower() == parent.lower() or
            self._would_create_invalid_parent_child_relationship(child, parent)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"parent({parent.lower()}, {child.lower()})")
        print("OK! I learned something.")

    def _process_daughter_statement(self, statement):
        """Process '[Name] is a daughter of [Name]' statement."""
        daughter, parent = self._extract_names_from_statement(statement, " is a daughter of ")
        
        if (daughter.lower() == parent.lower() or
            self._has_gender_conflict(daughter, 'female') or
            self._would_create_invalid_parent_child_relationship(daughter, parent)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"female({daughter.lower()})")
        self.prolog_engine.assertz(f"parent({parent.lower()}, {daughter.lower()})")
        print("OK! I learned something.")

    def _process_son_statement(self, statement):
        """Process '[Name] is a son of [Name]' statement."""
        son, parent = self._extract_names_from_statement(statement, " is a son of ")
        
        if (son.lower() == parent.lower() or
            self._has_gender_conflict(son, 'male') or
            self._would_create_invalid_parent_child_relationship(son, parent)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"male({son.lower()})")
        self.prolog_engine.assertz(f"parent({parent.lower()}, {son.lower()})")
        print("OK! I learned something.")

    def _process_aunt_statement(self, statement):
        """Process '[Name] is an aunt of [Name]' statement."""
        aunt, niece_or_nephew = self._extract_names_from_statement(statement, " is an aunt of ")
        
        if (aunt.lower() == niece_or_nephew.lower() or
            self._has_gender_conflict(aunt, 'female') or
            self._would_create_circular_relationship(niece_or_nephew, aunt)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"female({aunt.lower()})")
        self.prolog_engine.assertz(f"pibling({aunt.lower()}, {niece_or_nephew.lower()})")
        print("OK! I learned something.")

    def _process_uncle_statement(self, statement):
        """Process '[Name] is an uncle of [Name]' statement."""
        uncle, niece_or_nephew = self._extract_names_from_statement(statement, " is an uncle of ")
        
        if (uncle.lower() == niece_or_nephew.lower() or
            self._has_gender_conflict(uncle, 'male') or
            self._would_create_circular_relationship(niece_or_nephew, uncle)):
            print("That's impossible!")
            return
            
        self.prolog_engine.assertz(f"male({uncle.lower()})")
        self.prolog_engine.assertz(f"pibling({uncle.lower()}, {niece_or_nephew.lower()})")
        print("OK! I learned something.")

    def process_question(self, user_question):
        """
        Process a user question and provide an appropriate answer.
        
        Args:
            user_question (str): The question provided by the user
        """
        question = user_question.strip()
        
        try:
            # Yes/No questions - exact patterns from specifications
            if question.startswith("Are ") and " siblings?" in question:
                self._process_siblings_question(question)
            elif question.startswith("Is ") and " a sister of " in question and question.endswith("?"):
                self._process_sister_question(question)
            elif question.startswith("Is ") and " a brother of " in question and question.endswith("?"):
                self._process_brother_question(question)
            elif question.startswith("Is ") and " the mother of " in question and question.endswith("?"):
                self._process_mother_question(question)
            elif question.startswith("Is ") and " the father of " in question and question.endswith("?"):
                self._process_father_question(question)
            elif question.startswith("Are ") and " the parents of " in question and question.endswith("?"):
                self._process_parents_question(question)
            elif question.startswith("Is ") and " a grandmother of " in question and question.endswith("?"):
                self._process_grandmother_question(question)
            elif question.startswith("Is ") and " a grandfather of " in question and question.endswith("?"):
                self._process_grandfather_question(question)
            elif question.startswith("Is ") and " a daughter of " in question and question.endswith("?"):
                self._process_daughter_question(question)
            elif question.startswith("Is ") and " a son of " in question and question.endswith("?"):
                self._process_son_question(question)
            elif question.startswith("Is ") and " a child of " in question and question.endswith("?"):
                self._process_child_question(question)
            elif question.startswith("Are ") and " children of " in question and question.endswith("?"):
                self._process_multiple_children_question(question)
            elif question.startswith("Is ") and " an aunt of " in question and question.endswith("?"):
                self._process_aunt_question(question)
            elif question.startswith("Is ") and " an uncle of " in question and question.endswith("?"):
                self._process_uncle_question(question)
            elif question.startswith("Are ") and " relatives?" in question:
                self._process_relatives_question(question)
            
            # Who questions - exact patterns from specifications  
            elif question.startswith("Who are the siblings of ") and question.endswith("?"):
                self._process_who_siblings_question(question)
            elif question.startswith("Who are the sisters of ") and question.endswith("?"):
                self._process_who_sisters_question(question)
            elif question.startswith("Who are the brothers of ") and question.endswith("?"):
                self._process_who_brothers_question(question)
            elif question.startswith("Who is the mother of ") and question.endswith("?"):
                self._process_who_mother_question(question)
            elif question.startswith("Who is the father of ") and question.endswith("?"):
                self._process_who_father_question(question)
            elif question.startswith("Who are the parents of ") and question.endswith("?"):
                self._process_who_parents_question(question)
            elif question.startswith("Who are the daughters of ") and question.endswith("?"):
                self._process_who_daughters_question(question)
            elif question.startswith("Who are the sons of ") and question.endswith("?"):
                self._process_who_sons_question(question)
            elif question.startswith("Who are the children of ") and question.endswith("?"):
                self._process_who_children_question(question)
                
            else:
                print("Invalid question. Please follow the sentence patterns.")
                
        except Exception:
            print("Invalid question. Please follow the sentence patterns.")

    def _process_siblings_question(self, question):
        """Process 'Are [Name] and [Name] siblings?' question."""
        modified_question = question.replace("Are ", "").replace(" siblings?", "")
        parts = modified_question.split(" and ")
        
        if len(parts) == 2:
            person1 = parts[0].strip().lower().capitalize()
            person2 = parts[1].strip().lower().capitalize()
            result = self._is_fact_provable(f"sibling({person1.lower()}, {person2.lower()})")
            print("Yes!" if result else "No!")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def _process_sister_question(self, question):
        """Process 'Is [Name] a sister of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        person1, person2 = self._extract_names_from_statement(modified_question, " a sister of ")
        result = self._is_fact_provable(f"sister({person1.lower()}, {person2.lower()})")
        print("Yes!" if result else "No!")

    def _process_brother_question(self, question):
        """Process 'Is [Name] a brother of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        person1, person2 = self._extract_names_from_statement(modified_question, " a brother of ")
        result = self._is_fact_provable(f"brother({person1.lower()}, {person2.lower()})")
        print("Yes!" if result else "No!")

    def _process_mother_question(self, question):
        """Process 'Is [Name] the mother of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        parent, child = self._extract_names_from_statement(modified_question, " the mother of ")
        result = self._is_fact_provable(f"mother({parent.lower()}, {child.lower()})")
        print("Yes!" if result else "No!")

    def _process_father_question(self, question):
        """Process 'Is [Name] the father of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        parent, child = self._extract_names_from_statement(modified_question, " the father of ")
        result = self._is_fact_provable(f"father({parent.lower()}, {child.lower()})")
        print("Yes!" if result else "No!")

    def _process_parents_question(self, question):
        """Process 'Are [Name] and [Name] the parents of [Name]?' question."""
        modified_question = question.replace("Are ", "").replace(" the parents of ", " and ").replace("?", "")
        parts = modified_question.split(" and ")
        
        if len(parts) == 3:
            parent1 = parts[0].strip().lower()
            parent2 = parts[1].strip().lower()
            child = parts[2].strip().lower()
            
            result1 = self._is_fact_provable(f"parent({parent1}, {child})")
            result2 = self._is_fact_provable(f"parent({parent2}, {child})")
            print("Yes!" if (result1 and result2) else "No!")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def _process_grandmother_question(self, question):
        """Process 'Is [Name] a grandmother of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        grandparent, grandchild = self._extract_names_from_statement(modified_question, " a grandmother of ")
        result = self._is_fact_provable(f"grandmother({grandparent.lower()}, {grandchild.lower()})")
        print("Yes!" if result else "No!")

    def _process_grandfather_question(self, question):
        """Process 'Is [Name] a grandfather of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        grandparent, grandchild = self._extract_names_from_statement(modified_question, " a grandfather of ")
        result = self._is_fact_provable(f"grandfather({grandparent.lower()}, {grandchild.lower()})")
        print("Yes!" if result else "No!")

    def _process_daughter_question(self, question):
        """Process 'Is [Name] a daughter of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        child, parent = self._extract_names_from_statement(modified_question, " a daughter of ")
        result = self._is_fact_provable(f"daughter({child.lower()}, {parent.lower()})")
        print("Yes!" if result else "No!")

    def _process_son_question(self, question):
        """Process 'Is [Name] a son of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        child, parent = self._extract_names_from_statement(modified_question, " a son of ")
        result = self._is_fact_provable(f"son({child.lower()}, {parent.lower()})")
        print("Yes!" if result else "No!")

    def _process_child_question(self, question):
        """Process 'Is [Name] a child of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        child, parent = self._extract_names_from_statement(modified_question, " a child of ")
        result = self._is_fact_provable(f"parent({parent.lower()}, {child.lower()})")
        print("Yes!" if result else "No!")

    def _process_multiple_children_question(self, question):
        """Process 'Are [Name], [Name] and [Name] children of [Name]?' question."""
        modified_question = question.replace("Are ", "").replace(" children of ", " and ").replace("?", "").replace(", ", " and ")
        parts = modified_question.split(" and ")
        
        if len(parts) >= 2:
            children = [child.strip().lower() for child in parts[:-1]]
            parent = parts[-1].strip().lower()
            
            all_children = all(self._is_fact_provable(f"parent({parent}, {child})") for child in children)
            print("Yes!" if all_children else "No!")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def _process_aunt_question(self, question):
        """Process 'Is [Name] an aunt of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        aunt, niece_or_nephew = self._extract_names_from_statement(modified_question, " an aunt of ")
        result = self._is_fact_provable(f"aunt({aunt.lower()}, {niece_or_nephew.lower()})")
        print("Yes!" if result else "No!")

    def _process_uncle_question(self, question):
        """Process 'Is [Name] an uncle of [Name]?' question."""
        modified_question = question.replace("Is ", "").replace("?", "")
        uncle, niece_or_nephew = self._extract_names_from_statement(modified_question, " an uncle of ")
        result = self._is_fact_provable(f"uncle({uncle.lower()}, {niece_or_nephew.lower()})")
        print("Yes!" if result else "No!")

    def _process_relatives_question(self, question):
        """Process 'Are [Name] and [Name] relatives?' question."""
        modified_question = question.replace("Are ", "").replace(" relatives?", "")
        parts = modified_question.split(" and ")
        
        if len(parts) == 2:
            person1 = parts[0].strip().lower()
            person2 = parts[1].strip().lower()
            result = self._are_persons_related(person1, person2)
            print("Yes!" if result else "No!")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def _process_who_siblings_question(self, question):
        """Process 'Who are the siblings of [Name]?' question."""
        person = question.replace("Who are the siblings of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"sibling(X, {person})"))
        
        if results:
            # Remove duplicates by converting to set and back to list
            siblings = list(set([result['X'].capitalize() for result in results]))
            siblings.sort()  # Sort for consistent output
            print(f"The siblings of {person.capitalize()} are: {', '.join(siblings)}.")
        else:
            print(f"I don't know the siblings of {person.capitalize()}.")

    def _process_who_sisters_question(self, question):
        """Process 'Who are the sisters of [Name]?' question."""
        person = question.replace("Who are the sisters of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"sister(X, {person})"))
        
        if results:
            sisters = list(set([result['X'].capitalize() for result in results]))
            sisters.sort()
            print(f"The sisters of {person.capitalize()} are: {', '.join(sisters)}.")
        else:
            print(f"I don't know the sisters of {person.capitalize()}.")

    def _process_who_brothers_question(self, question):
        """Process 'Who are the brothers of [Name]?' question."""
        person = question.replace("Who are the brothers of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"brother(X, {person})"))
        
        if results:
            brothers = list(set([result['X'].capitalize() for result in results]))
            brothers.sort()
            print(f"The brothers of {person.capitalize()} are: {', '.join(brothers)}.")
        else:
            print(f"I don't know the brothers of {person.capitalize()}.")

    def _process_who_mother_question(self, question):
        """Process 'Who is the mother of [Name]?' question."""
        child = question.replace("Who is the mother of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"mother(X, {child})"))
        
        if results:
            mother = results[0]['X'].capitalize()
            print(f"The mother of {child.capitalize()} is {mother}.")
        else:
            print(f"I don't know who the mother of {child.capitalize()} is.")

    def _process_who_father_question(self, question):
        """Process 'Who is the father of [Name]?' question."""
        child = question.replace("Who is the father of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"father(X, {child})"))
        
        if results:
            father = results[0]['X'].capitalize()
            print(f"The father of {child.capitalize()} is {father}.")
        else:
            print(f"I don't know who the father of {child.capitalize()} is.")

    def _process_who_parents_question(self, question):
        """Process 'Who are the parents of [Name]?' question."""
        child = question.replace("Who are the parents of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"parent(X, {child})"))
        
        if results:
            parents = list(set([result['X'].capitalize() for result in results]))
            parents.sort()
            print(f"The parents of {child.capitalize()} are: {', '.join(parents)}.")
        else:
            print(f"I don't know the parents of {child.capitalize()}.")

    def _process_who_daughters_question(self, question):
        """Process 'Who are the daughters of [Name]?' question."""
        parent = question.replace("Who are the daughters of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"daughter(X, {parent})"))
        
        if results:
            daughters = list(set([result['X'].capitalize() for result in results]))
            daughters.sort()
            print(f"The daughters of {parent.capitalize()} are: {', '.join(daughters)}.")
        else:
            print(f"I don't know the daughters of {parent.capitalize()}.")

    def _process_who_sons_question(self, question):
        """Process 'Who are the sons of [Name]?' question."""
        parent = question.replace("Who are the sons of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"son(X, {parent})"))
        
        if results:
            sons = list(set([result['X'].capitalize() for result in results]))
            sons.sort()
            print(f"The sons of {parent.capitalize()} are: {', '.join(sons)}.")
        else:
            print(f"I don't know the sons of {parent.capitalize()}.")

    def _process_who_children_question(self, question):
        """Process 'Who are the children of [Name]?' question."""
        parent = question.replace("Who are the children of ", "").replace("?", "").strip().lower()
        results = list(self.prolog_engine.query(f"parent({parent}, X)"))
        
        if results:
            children = list(set([result['X'].capitalize() for result in results]))
            children.sort()
            print(f"The children of {parent.capitalize()} are: {', '.join(children)}.")
        else:
            print(f"I don't know the children of {parent.capitalize()}.")

    def start_conversation(self):
        """
        Start the main conversation loop for the chatbot.
        """
        print("\n------------------------------------------------------")
        print("|Hello there! This is the Family Relationship Chatbot|")
        print("------------------------------------------------------\n")
        print("Feel free to tell me statements or ask questions about family relationships. I will be happy to assist you:>\n")
        print("If you don't want to continue anymore, just enter 'quit' or 'exit' to end the conversation.")
        print()
        
        while True:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ["quit", "exit"]:
                print("Byebye:<")
                break
            elif "?" in user_input:
                self.process_question(user_input)
            else:
                self.process_statement(user_input)

if __name__ == "__main__":
    chatbot = FamilyRelationshipChatbot("chat.pl")
    chatbot.start_conversation()
