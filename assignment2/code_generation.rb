module Model
	def self.generate(filename)
		file = File.open(filename)
		list_of_lines = file.readlines
		title_line = list_of_lines[0].split(" ")
		title_line[1].slice! ":"
		class_name = title_line[1]

		attribute_hash = Hash.new()
		constraint_hash = Hash.new()

		for line in list_of_lines
			if line.start_with?("attribute")
				attribute_line = line.split(" ")
				attribute_line[1].slice! ":"
				attribute_line[1].slice! ","
				attribute_hash[attribute_line[1]] = attribute_line[2]
				constraint_hash[attribute_line[1]] = Array.new()	
			end
		end

		for line in list_of_lines
			if line.start_with?("constraint")
				line.slice! "constraint :"
				constraint_line = line.split(", ")
				value_array = constraint_hash[constraint_line[0]] 
				value_array << constraint_line[1]
			end
		end

		# create a new empty and nameless class 
		my_class = Class.new(Object) 

		# adding the nameless class to the constants will also make it take the name that we give it
		self.class.const_set(class_name, my_class)

		# Class has a private method "define_method". It could be used from another method inside the 
		# class itself, but since we weren't allowed to use "def" we can't define that other helper method.
		# Another way of circumventing information hiding that we have mentionet is the method "send"
		attribute_hash.each do |attribute, type|
			my_class.send(:define_method,(attribute+"=").to_sym, lambda{|arg|
			if arg.class.to_s == type
				constraint_array = constraint_hash[attribute]
				for constraint in constraint_array
					constraint.gsub! "\"", ""
					constraint.gsub! "\'", ""
					if arg.class == "String".class
						constraint.gsub! attribute, "\""+arg+"\"" 
					else
						constraint.gsub! attribute, arg.to_s
					end
					puts constraint
					puts eval(constraint)
					if not eval(constraint) 
						return # Throw RuntimeError instead
					end
				end
				eval("@#{attribute} = arg")
			end})
			my_class.send(:define_method, attribute.to_sym, lambda{
				eval("@#{attribute}")})
		end
	end
	mc = my_class.new
	mc.name=("Tobias")
	mc.age=(24)
	puts mc
	puts mc.name
	puts mc.age
end

person_class = Model.generate("Person.txt")

persons = person_class.load_from_file( ’entries.yml’ )
