class Array
	def select_first(**args)
		puts "Array: #{self}"
		puts "Arguments: #{args} | Args type: #{args.class} | Args size: #{args.length}"
		key,value = args.first
		puts "Value type: #{value.class} Length: #{value.length}"
				
		case value
			when Array
				self.each do |e|
					value.each do |i|
						if e.send(key) == i
							return e
						end
					end
				end
				exit
			
			when Hash
				min = value.has_key?(:min) ? value[:min] : 0
				max = value[:max]
				
				self.each do |e|
					attr = e.send(key)
					if attr >= min && attr <= max
						return e
					end
				end
						
				
				exit
			
			else 
				self.each do |e|
					if e.send(key) == value
						return e				
					end
				end
				return "No such element found"
		end
	end	
	
	def select_all(args)
		puts "Unimplemented method"
	end	
end

