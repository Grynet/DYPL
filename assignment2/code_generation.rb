require 'YAML'
module Model
	def self.generate(filepath)
		file = File.open(filepath)
		array_of_lines = file.readlines
		title_line = array_of_lines[0].split(" ")
		title_line[1].slice! ":"
		class_name = title_line[1]
		attribute_hash = Hash.new()
		constraint_hash = Hash.new()

		for line in array_of_lines
			if line.start_with?("attribute")
				attribute_line = line.split(" ")
				attribute_line[1].slice! ":"
				attribute_line[1].slice! ","
				attribute_hash[attribute_line[1]] = attribute_line[2]
				constraint_hash[attribute_line[1]] = Array.new()	
			end
		end
		for line in array_of_lines
			if line.start_with?("constraint")
				line.slice! "constraint :"
				constraint_line = line.split(", ")
				value_array = constraint_hash[constraint_line[0]] 
				value_array << constraint_line[1].strip
			end
		end

		# create a new empty and nameless class 
		my_class = Class.new

		# adding the nameless class to the constants will also make it take the name that we give it
		#self.class.const_set(class_name, my_class)
		my_class.class.const_set("#{class_name}", my_class)

		# Class has a private method "define_method". It could be used from another method inside the 
		# class itself, but since we weren't allowed to use "def" we can't define that other helper method.
		# Another way of circumventing information hiding that we have mentionet is the method "send"
		attribute_hash.each do |attribute, type|
			my_class.send(:define_method,(attribute+"=").to_sym, lambda{|arg|
			if arg.class.to_s == type
				constraint_array = constraint_hash[attribute]
				for constraint in constraint_array
					if constraint.start_with?("%{")
						constraint.sub! "%{", ""
						constraint.chop!
					end
					if constraint.start_with?("%(")
						constraint.sub! "%(", ""
						constraint.chop!
					end
					constraint.gsub! "\"", ""
					constraint.gsub! "\'", ""
					new_constraint = constraint
					if arg.class == "String".class
						new_constraint = constraint.gsub(attribute, "\""+arg+"\"")
					else
						new_constraint = constraint.gsub(attribute, arg.to_s)
					end
					if not eval(new_constraint) 
						raise #RuntimeError
					end
				end
				eval("@#{attribute} = arg")
			end})
			my_class.send(:define_method, attribute.to_sym, lambda{
				eval("@#{attribute}")})
		end
		my_class.send(:define_method, "load_from_file".to_sym, lambda{ | filepath |
			yamlContent = YAML.load_file(filepath)         
			object_array = Array.new
			yamlContent.each do | content |
				content[1].each do | entries |
					object = my_class.new
					exists = true
					entries.each do | key, value | 
						equation = ""
						check_variable = "object.#{key}"
						if value.class == Fixnum
							equation = "object.#{key}=(#{value})"
						else
							equation = "object.#{key}=('#{value}')"
						end
						if defined? eval("#{check_variable}") == method
							begin
								eval("#{equation}")
							rescue RuntimeError
								exists = false
							end
						else
							exists = false
						end
					end
					if exists
						object_array << object
					end
				end
			end
			return object_array
		})
		return my_class.new
	end


end